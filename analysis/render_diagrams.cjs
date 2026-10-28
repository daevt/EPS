const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { pathToFileURL } = require('node:url');
const os = require('node:os');
let playwright;
try { playwright = require('playwright-core'); }
catch { playwright = require(path.join(os.homedir(),'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright-core')); }
const { chromium } = playwright;

async function main() {
  const roots = process.argv.slice(2);
  const files = [];
  function collect(p) {
    if (fs.statSync(p).isDirectory()) {
      for (const name of fs.readdirSync(p)) collect(path.join(p,name));
    } else if (p.endsWith('.drawio')) files.push(path.resolve(p));
  }
  if (!roots.length || roots.includes('--current')) {
    const read=name=>JSON.parse(fs.readFileSync(path.join(__dirname,name),'utf8').replace(/^\uFEFF/,''));
    const relative = [
      ...read('overview_manifest.json').diagrams.map(d=>d.file),
      ...read('activity_models.json').diagrams.map(d=>d.filename),
      ...read('sequence_models.json').diagrams.map(d=>d.filename),
    ];
    relative.forEach(p=>files.push(path.resolve(__dirname,p)));
  } else roots.forEach(collect);
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
  const page = await browser.newPage({viewport:{width:2400,height:1800},deviceScaleFactor:1});
  await page.route('http://**/*', route=>route.abort());
  await page.route('https://**/*', route=>route.abort());
  await page.goto(pathToFileURL(path.join(__dirname,'vendor','drawio','viewer.html')).href);
  await page.waitForFunction(()=>window.drawioReady===true,{timeout:30000});
  const reports=[];
  for (const file of files) {
    const xml=fs.readFileSync(file,'utf8');
    const result=await page.evaluate(({xml})=>{
      const host=document.getElementById('graph');
      if(window.currentGraph) window.currentGraph.destroy();
      host.innerHTML=''; host.style.width='3000px';host.style.height='7000px';
      const doc=mxUtils.parseXml(xml);
      const model=doc.getElementsByTagName('mxGraphModel')[0];
      if(!model) throw Error('Missing graph model');
      const graph=new Graph(host);window.currentGraph=graph;graph.setEnabled(false);
      new mxCodec(doc).decode(model,graph.getModel());
      graph.getView().validate();
      const raw=graph.getGraphBounds();
      const nativeSvg=graph.getSvg('#ffffff',1,24);
      const svg=new XMLSerializer().serializeToString(nativeSvg);
      const cells=Object.values(graph.getModel().cells);
      const edges=cells.filter(c=>c.edge).map(c=>{
        const state=graph.getView().getState(c);
        return {id:c.id,source:c.source?.id,target:c.target?.id,
          points:state?.absolutePoints?.filter(Boolean).map(p=>({x:p.x,y:p.y})),
          label:state?.absoluteOffset?{x:state.absoluteOffset.x,y:state.absoluteOffset.y}:null,
          labelBox:state?.text?.boundingBox?{x:state.text.boundingBox.x,y:state.text.boundingBox.y,w:state.text.boundingBox.width,h:state.text.boundingBox.height}:null,
          paths:state?.shape?.node ? Array.from(state.shape.node.querySelectorAll('path')).map(p=>p.getAttribute('d')):[]};
      });
      const vertices=cells.filter(c=>c.vertex).map(c=>{
        const s=graph.getView().getState(c);
        return {id:c.id,parent:c.parent?.id,label:c.value,style:c.style,x:s?.x,y:s?.y,w:s?.width,h:s?.height,
          text:s?.text?.boundingBox?{x:s.text.boundingBox.x,y:s.text.boundingBox.y,w:s.text.boundingBox.width,h:s.text.boundingBox.height}:null};
      });
      const scale=Math.min(1.6,2100/(raw.width+48),3300/(raw.height+48));
      graph.getView().scaleAndTranslate(scale,24-raw.x,24-raw.y);
      graph.getView().validate();
      const bounds=graph.getGraphBounds();
      const width=Math.ceil(bounds.x+bounds.width+24*scale),height=Math.ceil(bounds.y+bounds.height+24*scale);
      host.style.width=width+'px';host.style.height=height+'px';
      return {svg,edges,vertices,raw:{x:raw.x,y:raw.y,w:raw.width,h:raw.height},width,height,
        nativeEdgeCount:edges.filter(e=>e.paths.length).length};
    },{xml});
    fs.writeFileSync(file.replace(/\.drawio$/,'.svg'),result.svg,'utf8');
    await page.setViewportSize({width:Math.max(800,result.width+20),height:Math.max(600,result.height+20)});
    await page.locator('#graph').screenshot({path:file.replace(/\.drawio$/,'.png'),animations:'disabled'});
    await page.pdf({path:file.replace(/\.drawio$/,'.pdf'),width:result.width+'px',height:result.height+'px',
      margin:{top:0,bottom:0,left:0,right:0},printBackground:true,pageRanges:'1'});
    const {svg,...dom}=result;
    dom.sourceSha256=crypto.createHash('sha256').update(xml).digest('hex');
    const domDir=path.join(__dirname,'.render-cache','dom');fs.mkdirSync(domDir,{recursive:true});
    fs.writeFileSync(path.join(domDir,path.basename(file).replace(/\.drawio$/,'.dom.json')),JSON.stringify(dom,null,2),'utf8');
    reports.push({file,vertices:result.vertices.length,edges:result.edges.length,nativeEdgeCount:result.nativeEdgeCount,
      width:result.width,height:result.height});
    console.log(path.basename(file)+': '+result.vertices.length+' vertices, '+result.edges.length+' native edges');
  }
  fs.writeFileSync(path.join(__dirname,'.render-cache','last-render.json'),JSON.stringify(reports,null,2));
  await browser.close();
}
main().catch(e=>{console.error(e);process.exit(1)});
