import fs from 'fs';
const {feature}=await import('/home/claude/experts-pin/fonts/node_modules/topojson-client/src/index.js');
const {geoAlbers,geoPath}=await import('/home/claude/experts-pin/fonts/node_modules/d3-geo/dist/d3-geo.mjs');
const topo=JSON.parse(fs.readFileSync('/home/claude/experts-pin/fonts/node_modules/us-atlas/states-10m.json'));
const skip=new Set(['Alaska','Hawaii','Puerto Rico','American Samoa','Guam','Commonwealth of the Northern Mariana Islands','United States Virgin Islands']);
const lower=feature(topo,topo.objects.states).features.filter(f=>!skip.has(f.properties.name));
const lit={'Arizona':'AZ','Texas':'TX','Montana':'MT','Missouri':'MO','Illinois':'IL','Ohio':'OH','South Carolina':'SC','Virginia':'VA','Maryland':'MD','Pennsylvania':'PA','New Jersey':'NJ','New York':'NY'};
const W=960,H=600, proj=geoAlbers().fitExtent([[4,4],[W-4,H-4]],{type:'FeatureCollection',features:lower}), path=geoPath(proj).digits(1);
let dim=''; const states=[];
for(const f of lower){const n=f.properties.name; dim+=path(f); if(lit[n]) states.push({ab:lit[n],d:path(f),c:path.centroid(f).map(v=>+v.toFixed(1))});}
// light order: west to east
states.sort((a,b)=>a.c[0]-b.c[0]);
fs.writeFileSync('map12.json',JSON.stringify({W,H,dim,states}));
console.log(states.map(s=>s.ab).join(' '), dim.length);
