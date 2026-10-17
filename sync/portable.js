/* Portable article records with causal history and explicit primary-device priority. */
(function(root){
'use strict';
const stable=value=>{if(Array.isArray(value))return value.map(stable);if(value&&typeof value==='object')return Object.fromEntries(Object.keys(value).sort().map(key=>[key,stable(value[key])]));return value;};
const equal=(a,b)=>JSON.stringify(stable(a))===JSON.stringify(stable(b));
function resolve(local,incoming){
 if(!local)return {record:incoming,reason:'new'};
 if(local.revision===incoming.revision||equal(local.value,incoming.value))return {record:local,reason:'same'};
 if(incoming.ancestors.includes(local.revision))return {record:incoming,reason:'newer'};
 if(local.ancestors.includes(incoming.revision))return {record:local,reason:'older'};
 if(local.role==='primary'&&incoming.role!=='primary')return {record:local,reason:'iMac'};
 if(incoming.role==='primary'&&local.role!=='primary')return {record:incoming,reason:'iMac'};
 return {record:null,reason:'conflict'};
}
function combine(local,incoming,choices={}){
 const records={...local},conflicts=[],decisions=[];
 for(const [key,record] of Object.entries(incoming)){
  const decision=resolve(local[key],record);
  if(!decision.record){if(choices[key]==='local')decision.record=local[key];else if(choices[key]==='incoming')decision.record=record;else conflicts.push(key);}
  if(decision.record)records[key]=decision.record;
  decisions.push({key,reason:decision.reason});
 }
 return {records,conflicts,decisions};
}
const api={stable,equal,resolve,combine};if(typeof module==='object'&&module.exports)module.exports=api;else root.ReaderPortable=api;
})(globalThis);
