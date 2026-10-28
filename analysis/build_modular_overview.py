"""Fresh modular UML use-case views from the approved EPS plan only."""
from pathlib import Path
import json, statistics, xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parent
OUT=BASE/'diagrams'/'overview';OUT.mkdir(parents=True,exist_ok=True)
ucs=json.loads((BASE/'content_user_buyer.json').read_text(encoding='utf-8'))['use_cases']
ucs+=json.loads((BASE/'content_seller_admin_payment.json').read_text(encoding='utf-8'))
names={u['id']:u['name'] for u in ucs}
FONT='fontFamily=Helvetica;fontSize=14;fontColor=#172b4d;'
manifest=[]
def document(key,title,w,h):
    mx=ET.Element('mxfile',host='app.diagrams.net',version='32.5.5',type='device')
    page=ET.SubElement(mx,'diagram',id='EPS-'+key,name=title)
    model=ET.SubElement(page,'mxGraphModel',dx=str(w),dy=str(h),grid='1',gridSize='10',guides='1',page='1',pageScale='1',pageWidth=str(w),pageHeight=str(h),background='#ffffff',math='0',shadow='0')
    root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    return mx,root
def vertex(root,i,label,style,x,y,w,h,parent='1'):
    cell=ET.SubElement(root,'mxCell',id=i,value=label,style=FONT+style,vertex='1',parent=parent)
    ET.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    return cell
def save(mx,key,title,ids,notes):
    ET.indent(mx,space='  ');file=OUT/(key+'.drawio')
    ET.ElementTree(mx).write(file,encoding='utf-8',xml_declaration=True)
    manifest.append({'id':key,'title':title,'file':str(file.relative_to(BASE)).replace('\\','/'),'use_cases':ids,'notes':notes,'provenance':'Newly authored from approved MVP plan; no old diagram input'})
def module(key,title,ids,mapping,right=(),reference_ids=(),note=''):
    all_ids=ids+list(reference_ids);height=max(560,130+140*len(all_ids))
    left=[a for a in mapping if a not in right];right=list(right);actor_y={}
    for side in [left,right]:
        last=160;desired=[]
        for a in side:
            ys=[220+140*all_ids.index(u) for u in mapping[a] if u in all_ids]
            desired.append((statistics.median(ys) if ys else 220,a))
        for center,a in sorted(desired):
            y=max(last,round((center-50)/10)*10);actor_y[a]=y;last=y+180;height=max(height,y+160-130)
    mx,root=document(key,title,1280,height+400)
    vertex(root,key+'-title',title,'text;html=1;align=center;fontSize=23;fontStyle=1;',260,20,760,55)
    vertex(root,key+'-scope','Academic simulation | full VND amount | referenced UC codes keep their identity','text;html=1;align=center;fontSize=13;',260,80,760,35)
    vertex(root,key+'-boundary','EPS MVP - '+title.split(' - ')[-1],'rounded=0;html=1;container=1;pointerEvents=0;fillColor=#ffffff;strokeColor=#64748b;strokeWidth=2;verticalAlign=top;align=center;spacingTop=15;fontStyle=1;',300,140,660,height)
    for index,uc in enumerate(all_ids):
        is_ref=uc in reference_ids
        c=vertex(root,key+'-UC-'+uc,uc+'  '+names[uc]+(' [reference]' if is_ref else ''),'ellipse;whiteSpace=wrap;html=1;fillColor='+('#f5f5f5' if is_ref else '#dae8fc')+';strokeColor='+('#666666' if is_ref else '#6c8ebf')+';spacing=12;',90,70+140*index,480,90,key+'-boundary')
        c.set('data-model-id',uc);c.set('data-provenance','Approved MVP plan; fresh authoring')
    labels={'Guest':'Guest','Buyer':'Buyer','Seller':'Seller','Admin':'Admin','Merchant':'Merchant /\nMarketplace','Bank':'Partner Bank\n(mock)','Gateway':'Payment Gateway\n(mock)'}
    for actor in mapping:
        x=1150 if actor in right else 60
        vertex(root,key+'-actor-'+actor,labels[actor],'shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;whiteSpace=wrap;strokeColor=#334155;fillColor=#ffffff;',x,actor_y[actor],60,100)
    for actor,targets in mapping.items():
        for uc in targets:
            if uc not in all_ids:continue
            left_side=actor not in right
            peers=[a for a,rows in mapping.items() if uc in rows and (a not in right)==left_side]
            slot=(peers.index(actor)+1)/(len(peers)+1)
            e=ET.SubElement(root,'mxCell',id=key+'-assoc-'+actor+'-'+uc,value='',style='edgeStyle=none;html=1;endArrow=none;startArrow=none;strokeColor=#64748b;'+f'exitX={1 if left_side else 0};exitY=0.5;entryX={0 if left_side else 1};entryY={slot:.4f};',edge='1',parent='1',source=key+'-actor-'+actor,target=key+'-UC-'+uc)
            ET.SubElement(e,'mxGeometry',relative='1',attrib={'as':'geometry'})
    if key=='UC_Buyer':
        e=ET.SubElement(root,'mxCell',id=key+'-include-B4-P2',value='\u00abinclude\u00bb',style='edgeStyle=none;html=1;endArrow=open;dashed=1;fontFamily=Helvetica;fontSize=13;labelBackgroundColor=#ffffff;exitX=0.5;exitY=1;entryX=0.5;entryY=0;',edge='1',parent='1',source=key+'-UC-B4',target=key+'-UC-P2')
        ET.SubElement(e,'mxGeometry',relative='1',attrib={'as':'geometry'})
    vertex(root,key+'-note',note,'rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;align=left;spacing=14;',300,height+190,660,110)
    save(mx,key,title,ids,note)
module('UC_Account','3.1a - Account access',['U1','U2','U3'],{'Guest':['U1','U2'],'Buyer':['U2','U3'],'Seller':['U2','U3'],'Admin':['U2','U3']},right=('Seller','Admin'),note='U1 creates ordinary human accounts with MFA enrollment. Admin is pre-provisioned. Merchant clients use separate client authentication, not human login/MFA.')
module('UC_SharedParty','3.1b - Shared escrow-party actions',['U4','U5','U6','U7','U8'],{'Buyer':['U4','U5','U6','U7','U8'],'Seller':['U4','U5','U6','U7','U8'],'Merchant':['U4']},right=('Merchant',),note='Merchant uses U4.API for its own client escrows only. U8 accepted refund invokes P3; an open dispute invalidates a pending refund proposal. No merchant refund/dispute authority.')
module('UC_Buyer','3.1c - Buyer journey',['B1','B2','B3','B4'],{'Buyer':['B1','B2','B3','B4'],'Merchant':['B1'],'Bank':['B3'],'Gateway':['B3']},right=('Merchant','Bank','Gateway'),reference_ids=('P2',),note='B1.API reuses B1 with seller-bound client authorization. P2 is a referenced reusable payment use case. B4 always invokes P2 after its state guard accepts the release decision.')
module('UC_Seller','3.1d - Seller journey',['S1','S2'],{'Seller':['S1','S2']},note='Seller accepts terms before funding. S2 records goods delivery or service completion and required evidence; it never proves payment completion or automatically releases funds.')
module('UC_Admin','3.1e - Administration',['A1','A2','A3','A4','A5'],{'Admin':['A1','A2','A3','A4','A5'],'Bank':['A5'],'Gateway':['A5']},right=('Bank','Gateway'),note='A1 accepts one reasoned full-release or full-refund decision and invokes P2 or P3. A5 queries unknown outcomes and retries only confirmed failures; it cannot manually mark a transfer successful.')
module('UC_Payment','3.1f - Payment integration',['P1','P2','P3'],{'Bank':['P1','P2','P3'],'Gateway':['P1','P3']},right=('Gateway',),note='P1 confirms actual mock receipt. P2 releases via Bank mock. P3 refunds through the original funding provider/source. Buyer/Admin decisions initiate P2/P3 indirectly; no internal EPS actor is invented.')
mx,root=document('UC_Overview','3.1 - EPS use-case module map',1100,1300)
vertex(root,'map-title','3.1  EPS MVP - Use-case Module Map','text;html=1;align=center;fontSize=24;fontStyle=1;',60,20,980,60)
vertex(root,'map-intro','22 unique use cases | 7 external actor roles | academic simulation','text;html=1;align=center;',60,90,980,40)
cards=[('User / shared','U1-U8','Account access (3.1a) + shared escrow actions (3.1b)','Guest, Buyer, Seller, Admin; Merchant for query only'),('Buyer','B1-B4','Create, cancel, fund and confirm acceptance (3.1c)','Buyer; Merchant create; Bank/Gateway funding'),('Seller','S1-S2','Accept terms and record delivery/service completion (3.1d)','Seller'),('Admin','A1-A5','Disputes, policy, dashboard, audit and reconciliation (3.1e)','Admin; Bank/Gateway reconciliation'),('Payment integration','P1-P3','Confirm funding, release and refund (3.1f)','Bank and Payment Gateway mocks')]
for i,(group,ids,summary,actors) in enumerate(cards):
    vertex(root,'module-'+str(i),group+'  ['+ids+']\n'+summary+'\nActors: '+actors,'rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;align=left;spacing=18;fontSize=16;',100,170+i*190,900,145)
vertex(root,'map-note','Navigation map only: the six focused UML views contain the normative use cases and associations.\nSame UC code denotes the same goal; referenced payment use cases are not counted twice.\nMerchant API variants B1.API / U4.API reuse the human-channel business contracts.','rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;align=left;spacing=16;',100,1150,900,120)
save(mx,'UC_Overview','3.1 - EPS use-case module map',list(names),'Navigation to six focused UML views')
(BASE/'overview_manifest.json').write_text(json.dumps({'diagrams':manifest,'unique_use_case_count':len(names),'unique_actor_count':7,'origin':'Fresh generation from approved plan; no old diagram source'},indent=2),encoding='utf-8')
print('Fresh modular overview:',len(manifest),'views;',len(names),'unique UCs')
