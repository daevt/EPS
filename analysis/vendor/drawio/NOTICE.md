# Native diagram renderer

The unmodified `viewer-static.min.js` bundle is from the official jgraph/drawio
release **v32.5.5**:

https://raw.githubusercontent.com/jgraph/drawio/v32.5.5/src/main/webapp/js/viewer-static.min.js

The accompanying `LICENSE` was retrieved from that release. The local
`viewer.html` is an EPS export harness. External HTTP/HTTPS requests are blocked
by the export script. Draw.io content is decoded and rendered by the native
Graph/mxCodec model; the diagrams are not flattened images inside XML.

Export requirements: Node.js, playwright-core and Chrome. Diagram generation
also uses the installed drawio-skill's `scripts/seqlayout.py`. Individual
`.drawio` files and the combined collection can be edited directly in
diagrams.net without these generation/export dependencies.
