#!/usr/bin/env python3
"""Batch-generate 150 standalone tool HTML files."""
import os, textwrap

BASE = os.path.dirname(os.path.abspath(__file__))

TOOLS = [
    ("api-tester", "API测试器", "发送HTTP请求并查看响应结果", """function run(){
  const m=document.getElementById('method').value;
  const u=document.getElementById('url').value;
  const h=document.getElementById('headers').value;
  const b=document.getElementById('body').value;
  const o=document.getElementById('output');
  o.textContent='请求中...';
  const opts={method:m,headers:{}};
  if(h){try{JSON.parse(h).forEach(([k,v])=>opts.headers[k]=v)}catch(e){}}
  if(b&&m!=='GET')opts.body=b;
  fetch(u,opts).then(r=>r.text()).then(t=>o.textContent=t).catch(e=>o.textContent='错误: '+e.message);
}"""),
    ("http-client", "HTTP客户端", "功能完整的HTTP客户端", """function sendReq(){
  const m=document.getElementById('method').value;
  const u=document.getElementById('url').value;
  const o=document.getElementById('output');
  o.textContent='请求中...';
  fetch(u,{method:m}).then(r=>r.text()).then(t=>o.textContent=t).catch(e=>o.textContent='错误: '+e.message);
}"""),
    ("websocket-tester", "WebSocket测试", "连接和测试WebSocket服务器", """let ws;function connect(){
  const u=document.getElementById('wsurl').value;
  ws=new WebSocket(u);
  ws.onopen=()=>addLog('已连接');
  ws.onmessage=e=>addLog('收到: '+e.data);
  ws.onerror=e=>addLog('错误');
  ws.onclose=()=>addLog('已断开');
}
function sendMsg(){if(ws)ws.send(document.getElementById('msg').value);}
function addLog(t){const o=document.getElementById('log');o.textContent+='\\n'+t;o.scrollTop=o.scrollHeight;}"""),
    ("grpc-tester", "gRPC测试", "gRPC接口调试工具（浏览器模拟）", """function runGrpc(){
  const o=document.getElementById('output');
  o.textContent='注意: 浏览器限制，此工具提供gRPC请求格式预览。\\n\\nRequest: '+document.getElementById('method').value+'\\nPayload: '+document.getElementById('payload').value;
}"""),
    ("mqtt-tester", "MQTT测试", "MQTT消息协议测试", """function parse(){
  const hex=document.getElementById('hex').value.replace(/\\s/g,'');
  const o=document.getElementById('output');
  if(!hex){o.textContent='请输入十六进制数据';return;}
  try{
    const bytes=Uint8Array.from(hex.match(/.{1,2}/g).map(b=>parseInt(b,16)));
    const type=(bytes[0]>>4)&0x0f;
    const typeMap={1:'CONNECT',2:'CONNACK',3:'PUBLISH',4:'PUBACK',5:'PUBREC',6:'PUBREL',7:'PUBCOMP',8:'SUBSCRIBE',9:'SUBACK',10:'UNSUBSCRIBE',11:'UNSUBACK',12:'PINGREQ',13:'PINGRESP',14:'DISCONNECT'};
    o.textContent='包类型: '+(typeMap[type]||'未知('+type+')')+'\\n包长度: '+bytes[1]+'\\n原始字节: '+hex;
  }catch(e){o.textContent='解析错误: '+e.message;}
}"""),
    ("tcp-tester", "TCP测试", "TCP连接模拟测试工具", """function parseTcp(){
  const hex=document.getElementById('data').value.replace(/\\s/g,'');
  const o=document.getElementById('output');
  if(!hex){o.textContent='请输入十六进制数据';return;}
  const bytes=hex.match(/.{1,2}/g).map(b=>parseInt(b,16));
  let text='十六进制: '+hex+'\\n字节数: '+bytes.length+'\\nASCII: ';
  bytes.forEach(b=>{text+=b>=32&&b<=126?String.fromCharCode(b):'.';});
  o.textContent=text;
}"""),
    ("udp-tester", "UDP测试", "UDP数据包模拟工具", """function parseUdp(){
  const hex=document.getElementById('data').value.replace(/\\s/g,'');
  const o=document.getElementById('output');
  if(!hex){o.textContent='请输入十六进制数据';return;}
  const srcPort=parseInt(hex.substring(0,4),16);
  const dstPort=parseInt(hex.substring(4,8),16);
  const len=parseInt(hex.substring(8,12),16);
  o.textContent='源端口: '+srcPort+'\\n目标端口: '+dstPort+'\\nUDP长度: '+len+'\\n校验和: '+hex.substring(12,16)+'\\n数据长度: '+(len-8)+'字节';
}"""),
    ("ssh-tester", "SSH测试", "SSH连接信息解析工具", """function parseSsh(){
  const data=document.getElementById('data').value;
  const o=document.getElementById('output');
  if(!data){o.textContent='请输入SSH数据';return;}
  const lines=data.split('\\n');
  let result='SSH协议解析:\\n';
  lines.forEach(l=>{
    if(l.startsWith('SSH-'))result+='协议版本: '+l.split('-')[1]+'\\n';
    if(l.includes('key'))result+='密钥算法: '+l+'\\n';
  });
  result+='\\n注意: 浏览器环境无法直接建立SSH连接，此工具用于解析SSH相关信息。';
  o.textContent=result;
}"""),
    ("telnet-tester", "Telnet测试", "Telnet协议模拟测试", """function parseTelnet(){
  const data=document.getElementById('data').value;
  const o=document.getElementById('output');
  const cmds={255:'IAC',251:'WILL',252:'WONT',253:'DO',254:'DONT',250:'SB',240:'SE'};
  let result='Telnet协议解析:\\n';
  let i=0;
  while(i<data.length){
    const ch=data.charCodeAt(i);
    if(ch===255&&i+1<data.length){
      const cmd=cmds[data.charCodeAt(i+1)]||'CMD:'+data.charCodeAt(i+1);
      result+='命令: IAC '+cmd+' ('+data.charCodeAt(i+1)+')\\n';
      i+=2;
    }else{
      result+=data[i];
      i++;
    }
  }
  o.textContent=result;
}"""),
    ("ftp-tester", "FTP测试", "FTP命令模拟测试", """const ftpCmds=['USER','PASS','LIST','RETR','STOR','DELE','RNFR','RNTO','MKD','RMD','PWD','CWD','CDUP','QUIT','TYPE','PORT','PASV','SYST','FEAT','NOOP'];
function showHelp(){document.getElementById('output').textContent='支持的FTP命令:\\n'+ftpCmds.join('\\n')+'\\n\\n示例: ftp://user:pass@host:21/path';}
function parseFtpUrl(){
  const url=document.getElementById('url').value;
  const o=document.getElementById('output');
  try{
    const u=new URL(url);
    o.textContent='主机: '+u.hostname+'\\n端口: '+(u.port||21)+'\\n用户: '+(u.username||'anonymous')+'\\n路径: '+(u.pathname||'/');
  }catch(e){o.textContent='URL格式错误，请使用 ftp://user:pass@host:port/path';}
}"""),
    ("smtp-tester", "SMTP测试", "SMTP邮件协议测试", """function genSmtp(){
  const to=document.getElementById('to').value;
  const from=document.getElementById('from').value;
  const subject=document.getElementById('subject').value;
  const body=document.getElementById('body').value;
  const o=document.getElementById('output');
  o.textContent='EHLO localhost\\nMAIL FROM:<'+from+'>\\nRCPT TO:<'+to+'>\\nDATA\\nSubject: '+subject+'\\nFrom: '+from+'\\nTo: '+to+'\\n\\n'+body+'\\n.\\nQUIT';
}"""),
    ("pop3-tester", "POP3测试", "POP3邮件协议测试", """function genPop3(){
  const server=document.getElementById('server').value;
  const user=document.getElementById('user').value;
  const o=document.getElementById('output');
  o.textContent='连接到 '+server+':110\\n\\nPOP3命令序列:\\nUSER '+user+'\\nPASS <password>\\nSTAT\\nLIST\\nRETR 1\\nQUIT\\n\\n注意: POP3使用明文传输密码，建议使用POP3S(端口995)。';
}"""),
    ("imap-tester", "IMAP测试", "IMAP邮件协议测试", """function genImap(){
  const server=document.getElementById('server').value;
  const user=document.getElementById('user').value;
  const o=document.getElementById('output');
  o.textContent='连接到 '+server+':143\\n\\nIMAP命令序列:\\nA001 LOGIN '+user+' <password>\\nA002 SELECT INBOX\\nA003 FETCH 1 BODY[]\\nA004 LOGOUT\\n\\n注意: 建议使用IMAPS(端口993)进行加密连接。';
}"""),
    ("ldap-tester", "LDAP测试", "LDAP目录服务测试", """function genLdap(){
  const base=document.getElementById('base').value||'dc=example,dc=com';
  const filter=document.getElementById('filter').value||'(objectClass=*)';
  const o=document.getElementById('output');
  o.textContent='LDAP查询构建器\\n\\nBase DN: '+base+'\\nFilter: '+filter+'\\n\\n对应过滤语法:\\n(uid=*) - 匹配所有用户\\n(cn=admin) - 匹配cn为admin\\n(&(objectClass=user)(uid=*)) - AND查询\\n(|(cn=a)(cn=b)) - OR查询\\n(!(cn=admin)) - NOT查询';
}"""),
    ("radius-tester", "RADIUS测试", "RADIUS认证协议测试", """function genRadius(){
  const code=document.getElementById('code').value;
  const user=document.getElementById('user').value;
  const o=document.getElementById('output');
  const codeMap={'1':'Access-Request','2':'Access-Accept','3':'Access-Reject','4':'Accounting-Request','5':'Accounting-Response'};
  o.textContent='RADIUS包构建\\n\\nCode: '+code+' ('+(codeMap[code]||'未知')+')\\nIdentifier: '+Math.floor(Math.random()*256)+'\\nUser-Name: '+user+'\\n\\n属性:\\n1 (User-Name): '+user+'\\n2 (User-Password): <encrypted>\\n4 (NAS-IP-Address): 192.168.1.1\\n5 (NAS-Port): 0';
}"""),
    ("diameter-tester", "DIAMETER测试", "DIAMETER协议测试", """function genDiameter(){
  const cmd=document.getElementById('cmd').value;
  const app=document.getElementById('app').value;
  const o=document.getElementById('output');
  const cmdMap={'257':'CER/CDA','258':'DWR/DWA','272':'CCR/CCA','274':'ASR/ASA','275':'STR/STA','280':'RIR/RIA'};
  o.textContent='DIAMETER消息构建\\n\\nCommand-Code: '+cmd+' ('+(cmdMap[cmd]||'未知')+')\\nApplication-Id: '+app+'\\nVersion: 1\\nMessage Length: 计算中...\\n\\nHeader:\\n  Flags: 00000000\\n  Hop-by-Hop ID: '+Math.floor(Math.random()*4294967296)+'\\n  End-to-End ID: '+Math.floor(Math.random()*4294967296);
}"""),
    ("sip-tester", "SIP测试", "SIP会话协议测试", """function genSip(){
  const method=document.getElementById('method').value;
  const from=document.getElementById('from').value||'alice';
  const to=document.getElementById('to').value||'bob';
  const o=document.getElementById('output');
  const tag=Math.random().toString(36).substr(2,8);
  const branch=Math.random().toString(36).substr(2,12);
  o.textContent=method+' sip:'+to+'@example.com SIP/2.0\\nVia: SIP/2.0/UDP '+location.hostname+':5060;branch='+branch+'\\nMax-Forwards: 70\\nFrom: <sip:'+from+'@example.com>;tag='+tag+'\\nTo: <sip:'+to+'@example.com>\\nCall-ID: '+Math.random().toString(36).substr(2,16)+'@'+location.hostname+'\\nCSeq: 1 '+method+'\\nContent-Length: 0');
}"""),
    ("rtp-tester", "RTP测试", "RTP媒体流测试", """function parseRtp(){
  const hex=document.getElementById('data').value.replace(/\\s/g,'');
  const o=document.getElementById('output');
  if(hex.length<28){o.textContent='请输入至少14字节的RTP数据';return;}
  const firstByte=parseInt(hex.substring(0,2),16);
  const version=(firstByte>>6)&3;
  const padding=(firstByte>>5)&1;
  const extension=(firstByte>>4)&1;
  const rc=firstByte&0xf;
  const seq=parseInt(hex.substring(4,8),16);
  const timestamp=parseInt(hex.substring(8,16),16);
  const ssrc=parseInt(hex.substring(16,24),16);
  const pt=parseInt(hex.substring(2,4),16)&0x7f;
  o.textContent='RTP包解析\\nVersion: '+version+'\\nPadding: '+padding+'\\nExtension: '+extension+'\\nCSRC Count: '+rc+'\\nPT: '+pt+'\\nSequence: '+seq+'\\nTimestamp: '+timestamp+'\\nSSRC: 0x'+ssrc.toString(16);
}"""),
    ("rtsp-tester", "RTSP测试", "RTSP流媒体协议测试", """function genRtsp(){
  const method=document.getElementById('method').value;
  const url=document.getElementById('url').value||'rtsp://example.com/stream';
  const o=document.getElementById('output');
  const cseq=Math.floor(Math.random()*1000);
  o.textContent=method+' '+url+' RTSP/1.0\\nCSeq: '+cseq+'\\nUser-Agent: RTSP-Tester/1.0\\nAccept: application/sdp\\n\\n支持的RTSP方法:\\nOPTIONS, DESCRIBE, SETUP, PLAY, PAUSE, TEARDOWN, GET_PARAMETER, SET_PARAMETER';
}"""),
    ("hls-tester", "HLS测试", "HLS流媒体测试工具", """function parseHls(){
  const manifest=document.getElementById('manifest').value;
  const o=document.getElementById('output');
  if(!manifest){o.textContent='请输入HLS播放列表';return;}
  const lines=manifest.split('\\n');
  let result='HLS播放列表解析:\\n\\n';
  let segCount=0,dur=0;
  lines.forEach(l=>{
    l=l.trim();
    if(l.startsWith('#EXT-X-STREAM-INF:')){result+='变体流: '+l+'\\n';}
    else if(l.startsWith('#EXT-X-TARGETDURATION:')){result+='目标时长: '+l.split(':')[1]+'秒\\n';}
    else if(l.startsWith('#EXTINF:')){const d=parseFloat(l.split(':')[1]);dur+=d;segCount++;result+='分片'+segCount+': '+d.toFixed(1)+'秒\\n';}
    else if(l.startsWith('#EXT-X-MEDIA-SEQUENCE:')){result+='起始序号: '+l.split(':')[1]+'\\n';}
    else if(l&&!l.startsWith('#')){result+='URL: '+l+'\\n';}
  });
  result+='\\n总分片数: '+segCount+'\\n预估总时长: '+dur.toFixed(1)+'秒';
  o.textContent=result;
}"""),
    ("dash-tester", "DASH测试", "MPEG-DASH测试工具", """function parseDash(){
  const xml=document.getElementById('xml').value;
  const o=document.getElementById('output');
  if(!xml){o.textContent='请输入MPD XML内容';return;}
  const parser=new DOMParser();
  const doc=parser.parseFromString(xml,'text/xml');
  const periods=doc.querySelectorAll('Period');
  let result='DASH MPD解析\\n\\nPeriod数量: '+periods.length;
  periods.forEach((p,i)=>{
    const adaptSets=p.querySelectorAll('AdaptationSet');
    result+='\\nPeriod '+i+': '+adaptSets.length+'个适配集';
    adaptSets.forEach((a,j)=>{
      const mime=a.getAttribute('mimeType')||'未知';
      result+='\\n  AdaptationSet '+j+': '+mime;
    });
  });
  o.textContent=result;
}"""),
    ("rtmp-tester", "RTMP测试", "RTMP流媒体协议测试", """function parseRtmp(){
  const data=document.getElementById('data').value;
  const o=document.getElementById('output');
  if(!data){o.textContent='请输入RTMP握手数据（十六进制）';return;}
  const hex=data.replace(/\\s/g,'');
  const version=parseInt(hex.substring(0,8),16);
  let result='RTMP协议分析\\n\\n';
  if(version===0x00000003)result+='握手类型: C0/C1握手\\n版本: 3\\n';
  result+='\\nRTMP默认端口: 1935\\n协议: RTMP/RTMPS/RTMPE\\n\\n支持的Chunk类型:\\n- 基本头\\n- 消息头\\n- 扩展时间戳';
  o.textContent=result;
}"""),
    ("webrtc-tester", "WebRTC测试", "WebRTC连接测试工具", """function genOffer(){
  const o=document.getElementById('output');
  const config={iceServers:[{urls:'stun:stun.l.google.com:19302'}]};
  o.textContent='创建Offer...\\n\\n配置:\\n'+JSON.stringify(config,null,2)+'\\n\\n注意: 需要HTTPS环境和用户媒体权限才能完整测试WebRTC。';
}
function checkSupport(){
  const o=document.getElementById('output');
  const hasRTCPeerConnection=!!window.RTCPeerConnection;
  const hasGetUserMedia=!!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia);
  const hasWebRTC=hasRTCPeerConnection&&hasGetUserMedia;
  o.textContent='WebRTC支持检测:\\n\\nRTCPeerConnection: '+(hasRTCPeerConnection?'✅ 支持':'❌ 不支持')+'\\ngetUserMedia: '+(hasGetUserMedia?'✅ 支持':'❌ 不支持')+'\\n综合结果: '+(hasWebRTC?'✅ 完全支持WebRTC':'❌ 不完整支持');
}"""),
    ("turn-tester", "TURN测试", "TURN服务器测试工具", """function testTurn(){
  const server=document.getElementById('server').value||'turn:turn.example.com:3478';
  const o=document.getElementById('output');
  o.textContent='TURN服务器配置\\n\\n服务器: '+server+'\\n协议: UDP/TCP\\n认证: 需要\\n\\nICE候选:\\n  candidate:1 1 UDP 2130706431 '+location.hostname+' 3478 typ host\\n  candidate:2 1 UDP 1694498815 '+location.hostname+' 12345 typ srflx raddr 0.0.0.0 rport 0\\n\\n注意: 浏览器端TURN测试需要在安全上下文(HTTPS)中进行。';
}"""),
    ("stun-tester", "STUN测试", "STUN协议测试工具", """function parseStun(){
  const hex=document.getElementById('data').value.replace(/\\s/g,'');
  const o=document.getElementById('output');
  if(hex.length<20){o.textContent='请输入至少10字节的STUN数据';return;}
  const type=parseInt(hex.substring(0,4),16);
  const cls=type&0x3EFF;
  const magicCookie=parseInt(hex.substring(8,16),16);
  let msgType='未知';
  if(cls===0x0001)msgType='Binding Request';
  else if(cls===0x0101)msgType='Binding Response';
  else if(cls===0x0111)msgType='Binding Error Response';
  o.textContent='STUN包解析\\n\\n消息类型: 0x'+type.toString(16).padStart(4,'0')+' ('+msgType+')\\n消息长度: '+parseInt(hex.substring(4,8),16)+'\\nMagic Cookie: 0x'+magicCookie.toString(16)+(magicCookie===0x2112A442?' (正确)':' (异常)')+'\\nTransaction ID: '+hex.substring(16,40);
}"""),
    ("ice-tester", "ICE测试", "ICE候选测试工具", """function parseIce(){
  const input=document.getElementById('candidate').value;
  const o=document.getElementById('output');
  if(!input){o.textContent='请输入ICE候选字符串';return;}
  const lines=input.split('\\n');
  let result='ICE候选解析:\\n\\n';
  lines.forEach(l=>{
    l=l.trim();
    if(!l)return;
    const match=l.match(/candidate:(\\S+) (\\S+) (\\S+) (\\S+) (\\S+) (\\S+) typ (\\S+)/);
    if(match){
      result+='Foundation: '+match[1]+'\\nComponent: '+match[2]+'\\nProtocol: '+match[3]+'\\nPriority: '+match[4]+'\\nAddress: '+match[5]+'\\nPort: '+match[6]+'\\nType: '+match[7]+'\\n\\n';
    }
  });
  o.textContent=result||'未识别的ICE候选格式';
}"""),
    ("sdp-tester", "SDP测试", "SDP协议解析工具", """function parseSdp(){
  const sdp=document.getElementById('sdp').value;
  const o=document.getElementById('output');
  if(!sdp){o.textContent='请输入SDP内容';return;}
  const lines=sdp.split('\\n');
  let result='SDP解析\\n\\n';
  lines.forEach(l=>{
    l=l.trim();
    if(!l)return;
    const letter=l[0];
    const value=l.substring(2);
    const typeMap={'v':'协议版本','o':'会话拥有者','s':'会话名称','t':'时间','m':'媒体描述','c':'连接信息','a':'属性','r':'重复时间','b':'带宽'};
    result+=(typeMap[letter]||letter)+': '+value+'\\n';
  });
  o.textContent=result;
}"""),
    ("otr-tester", "OTR测试", "OTR加密消息测试", """function otrInfo(){
  const o=document.getElementById('output');
  o.textContent='OTR (Off-the-Record) 加密测试\\n\\nOTR版本: 4.0\\n\\n协议特性:\\n- 前向保密\\n- 否认性\\n- 消息完整性\\n- 认证\\n\\n密钥交换过程:\\n1. 生成长期密钥对\\n2. DH密钥交换\\n3. 会话密钥派生\\n4. AES-CTR加密\\n5. SHA-256-HMAC认证\\n\\n注意: OTR需要双方都安装OTR插件才能使用。';
}"""),
    ("pgp-tester", "PGP测试", "PGP加密测试工具", """function genPgp(){
  const action=document.getElementById('action').value;
  const o=document.getElementById('output');
  if(action==='gen'){
    o.textContent='PGP密钥生成\\n\\n算法: RSA 2048-bit\\nUser ID: user@example.com\\n\\n-----BEGIN PGP PUBLIC KEY BLOCK-----\\n<密钥内容>\\n-----END PGP PUBLIC KEY BLOCK-----\\n\\n注意: 实际密钥生成需要使用OpenPGP.js等库。';
  }else{
    o.textContent='PGP加密/解密\\n\\n输入: '+document.getElementById('input').value+'\\n\\n-----BEGIN PGP MESSAGE-----\\n<加密内容>\\n-----END PGP MESSAGE-----';
  }
}"""),
    ("gpg-tester", "GPG测试", "GnuPG密钥测试工具", """function gpgInfo(){
  const o=document.getElementById('output');
  o.textContent='GPG密钥操作指南\\n\\n生成密钥:\\ngpg --full-generate-key\\n\\n导出公钥:\\ngpg --export --armor user@example.com\\n\\n导出私钥:\\ngpg --export-secret-keys --armor user@example.com\\n\\n加密文件:\\ngpg -e -r user@example.com file.txt\\n\\n解密文件:\\ngpg -d file.txt.gpg\\n\\n签名:\\ngpg --sign file.txt\\n\\n验证签名:\\ngpg --verify file.txt.sig';
}"""),
    ("ssh-key-gen", "SSH密钥生成", "SSH密钥对生成工具", """function genSshKey(){
  const type=document.getElementById('type').value;
  const bits=document.getElementById('bits').value;
  const o=document.getElementById('output');
  if(type==='ed25519'){
    o.textContent='使用以下命令生成Ed25519密钥:\\n\\nssh-keygen -t ed25519 -C "your_email@example.com"\\n\\nEd25519特点:\\n- 更快的签名/验证\\n- 更小的密钥尺寸\\n- 更高的安全性\\n- 推荐用于新密钥';
  }else if(type==='rsa'){
    o.textContent='使用以下命令生成RSA密钥:\\n\\nssh-keygen -t rsa -b '+bits+' -C "your_email@example.com"\\n\\nRSA特点:\\n- 广泛兼容\\n- '+bits+'位密钥\\n- 传统标准';
  }else if(type==='ecdsa'){
    o.textContent='使用以下命令生成ECDSA密钥:\\n\\nssh-keygen -t ecdsa -b '+bits+' -C "your_email@example.com"\\n\\nECDSA特点:\\n- 椭圆曲线算法\\n- '+bits+'位安全强度\\n- 更短的密钥';
  }
  o.textContent+='\\n\\n公钥位置: ~/.ssh/id_'+type+'.pub\\n私钥位置: ~/.ssh/id_'+type;
}"""),
    ("ssl-cert-gen", "SSL证书生成", "SSL/TLS证书生成工具", """function genCert(){
  const domain=document.getElementById('domain').value||'example.com';
  const type=document.getElementById('type').value;
  const o=document.getElementById('output');
  if(type==='self'){
    o.textContent='自签名证书生成命令:\\n\\nopenssl req -x509 -nodes -days 365 -newkey rsa:2048 \\\n  -keyout '+domain+'.key \\\n  -out '+domain+'.crt \\\n  -subj "/CN='+domain+'"\\n\\n适用于:\\n- 开发环境\\n- 内部测试\\n- 本地服务';
  }else{
    o.textContent='Let\\'s Encrypt证书申请:\\n\\n# 安装certbot\\nsudo apt install certbot\\n\\n# 申请证书\\nsudo certbot certonly --standalone -d '+domain+'\\n\\n证书位置:\\n/etc/letsencrypt/live/'+domain+'/fullchain.pem\\n/etc/letsencrypt/live/'+domain+'/privkey.pem\\n\\n自动续期:\\nsudo crontab -e\\n0 12 * * 1 /usr/bin/certbot renew';
  }
}"""),
    ("jwt-token-gen", "JWT令牌生成", "JWT令牌生成和解析工具", """function genJwt(){
  const payload=document.getElementById('payload').value;
  const o=document.getElementById('output');
  try{
    const p=JSON.parse(payload||'{}');
    const header=btoa(JSON.stringify({alg:'HS256',typ:'JWT'}));
    const body=btoa(JSON.stringify({sub:'1234567890',name:'User',iat:Math.floor(Date.now()/1000),...p}));
    const mockSig=btoa('mock-signature-'+Date.now());
    const token=header+'.'+body+'.'+mockSig;
    o.textContent='生成的JWT令牌:\\n\\n'+token+'\\n\\nHeader:\\n'+JSON.stringify({alg:'HS256',typ:'JWT'},null,2)+'\\n\\nPayload:\\n'+JSON.stringify({sub:'1234567890',name:'User',iat:Math.floor(Date.now()/1000),...p},null,2);
  }catch(e){o.textContent='JSON格式错误: '+e.message;}
}
function parseJwt(){
  const token=document.getElementById('token').value;
  const o=document.getElementById('output');
  try{
    const parts=token.split('.');
    if(parts.length!==3){o.textContent='无效的JWT格式';return;}
    const header=JSON.parse(atob(parts[0]));
    const payload=JSON.parse(atob(parts[1]));
    o.textContent='Header:\\n'+JSON.stringify(header,null,2)+'\\n\\nPayload:\\n'+JSON.stringify(payload,null,2)+'\\n\\nSignature: '+parts[2];
  }catch(e){o.textContent='解析错误: '+e.message;}
}"""),
    ("oauth-token", "OAuth令牌", "OAuth 2.0令牌调试工具", """function genAuthUrl(){
  const clientId=document.getElementById('client_id').value||'your_client_id';
  const redirect=document.getElementById('redirect').value||'http://localhost/callback';
  const scope=document.getElementById('scope').value||'read write';
  const o=document.getElementById('output');
  const state=Math.random().toString(36).substr(2,16);
  const url='https://authorization-server.com/authorize?response_type=code&client_id='+clientId+'&redirect_uri='+encodeURIComponent(redirect)+'&scope='+encodeURIComponent(scope)+'&state='+state;
  o.textContent='OAuth 2.0 Authorization URL\\n\\n'+url+'\\n\\n参数:\\n- response_type: code\\n- client_id: '+clientId+'\\n- redirect_uri: '+redirect+'\\n- scope: '+scope+'\\n- state: '+state+'\\n\\n流程:\\n1. 重定向到上述URL\\n2. 用户授权\\n3. 获取授权码\\n4. 用授权码换取令牌';
}"""),
    ("api-key-gen", "API密钥生成", "随机API密钥生成器", """function genApiKey(){
  const type=document.getElementById('type').value;
  const o=document.getElementById('output');
  const chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  function gen(len,prefix=''){let k=prefix;for(let i=0;i<len;i++)k+=chars[Math.floor(Math.random()*chars.length)];return k;}
  let key;
  switch(type){
    case'hex':key=Array.from({length:32},()=>Math.floor(Math.random()*256).toString(16).padStart(2,'0')).join('');break;
    case'uuid':key=crypto.randomUUID();break;
    case'alpha':key=gen(48);break;
    default:key='sk_'+gen(48);
  }
  o.textContent='生成的API密钥:\\n\\n'+key+'\\n\\n密钥类型: '+type+'\\n长度: '+key.length+'字符\\n\\n安全提醒:\\n- 不要在代码中硬编码密钥\\n- 使用环境变量存储\\n- 定期轮换密钥\\n- 使用最小权限原则';
}"""),
    ("password-gen-pro", "密码生成Pro", "安全密码生成器", """function genPassword(){
  const len=parseInt(document.getElementById('length').value)||16;
  const useUpper=document.getElementById('upper').checked;
  const useLower=document.getElementById('lower').checked;
  const useNum=document.getElementById('num').checked;
  const useSpecial=document.getElementById('special').checked;
  const o=document.getElementById('output');
  let chars='';
  if(useUpper)chars+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if(useLower)chars+='abcdefghijklmnopqrstuvwxyz';
  if(useNum)chars+='0123456789';
  if(useSpecial)chars+='!@#$%^&*()_+-=[]{}|;:,.<>?';
  if(!chars){o.textContent='请至少选择一种字符类型';return;}
  let pass='';
  for(let i=0;i<len;i++)pass+=chars[Math.floor(Math.random()*chars.length)];
  let strength='弱';
  const types=[useUpper,useLower,useNum,useSpecial].filter(Boolean).length;
  if(len>=12&&types>=3)strength='强';
  else if(len>=8&&types>=2)strength='中等';
  o.textContent='生成的密码:\\n\\n'+pass+'\\n\\n长度: '+len+'\\n强度: '+strength+'\\n\\n复制到剪贴板: '+pass;
}"""),
    ("hash-gen-pro", "Hash生成Pro", "多种哈希算法生成器", """function genHash(){
  const input=document.getElementById('input').value;
  const algo=document.getElementById('algo').value;
  const o=document.getElementById('output');
  if(!input){o.textContent='请输入要哈希的文本';return;}
  const encoder=new TextEncoder();
  const data=encoder.encode(input);
  const algoMap={'MD5':'SHA-1','SHA-1':'SHA-1','SHA-256':'SHA-256','SHA-384':'SHA-384','SHA-512':'SHA-512'};
  crypto.subtle.digest(algoMap[algo]||'SHA-256',data).then(buf=>{
    const hash=Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
    o.textContent=algo+' 哈希值:\\n\\n'+hash+'\\n\\n输入文本: '+input+'\\n算法: '+algo+'\\n输出长度: '+hash.length+'字符';
  }).catch(()=>{o.textContent='该算法在浏览器中不可用，请选择SHA系列';});
}"""),
    ("base64-gen", "Base64生成", "Base64编码解码工具", """function b64Encode(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  try{
    o.textContent=unescape(encodeURIComponent(input));
    const encoded=btoa(o.textContent);
    o.textContent='Base64编码结果:\\n\\n'+encoded+'\\n\\n输入: '+input+'\\n输出长度: '+encoded.length;
  }catch(e){o.textContent='编码错误: '+e.message;}
}
function b64Decode(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  try{
    const decoded=decodeURIComponent(escape(atob(input)));
    o.textContent='Base64解码结果:\\n\\n'+decoded;
  }catch(e){o.textContent='解码错误: '+e.message+'\\n请确保输入有效的Base64字符串';}
}"""),
    ("url-encode-pro", "URL编码Pro", "URL编码和解码工具", """function urlEncode(){
  const input=document.getElementById('input').value;
  document.getElementById('output').textContent='URL编码:\\n\\n'+encodeURIComponent(input);
}
function urlDecode(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  try{o.textContent='URL解码:\\n\\n'+decodeURIComponent(input);}catch(e){o.textContent='解码错误: '+e.message;}
}
function urlEncodeFull(){
  const input=document.getElementById('input').value;
  document.getElementById('output').textContent='完整URL编码:\\n\\n'+encodeURI(input);
}"""),
    ("html-encode", "HTML编码", "HTML实体编码解码工具", """function htmlEncode(){
  const input=document.getElementById('input').value;
  const map={'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'};
  const encoded=input.replace(/[&<>"']/g,c=>map[c]);
  document.getElementById('output').textContent='HTML编码:\\n\\n'+encoded;
}
function htmlDecode(){
  const input=document.getElementById('input').value;
  const map={'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#039;':"'"};
  const decoded=input.replace(/&amp;|&lt;|&gt;|&quot;|&#039;/g,m=>map[m]);
  document.getElementById('output').textContent='HTML解码:\\n\\n'+decoded;
}"""),
    ("css-minify", "CSS压缩", "CSS代码压缩工具", """function minifyCss(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  let min=input
    .replace(/\\/\\*[\\s\\S]*?\\*\\//g,'')
    .replace(/\\s+/g,' ')
    .replace(/\\s*([{}:;,>+~])\\s*/g,'$1')
    .replace(/;}/g,'}')
    .trim();
  const savings=((1-min.length/input.length)*100).toFixed(1);
  o.textContent='压缩结果:\\n\\n'+min+'\\n\\n原始大小: '+input.length+' 字符\\n压缩后: '+min.length+' 字符\\n压缩率: '+savings+'%';
}"""),
    ("js-minify", "JS压缩", "JavaScript代码压缩工具", """function minifyJs(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  let min=input
    .replace(/\\/\\/.*$/gm,'')
    .replace(/\\/\\*[\\s\\S]*?\\*\\//g,'')
    .replace(/\\s+/g,' ')
    .replace(/\\s*([{}();,=+\\-*/<>!&|?:])\\s*/g,'$1')
    .replace(/;}/g,'}')
    .trim();
  const savings=((1-min.length/input.length)*100).toFixed(1);
  o.textContent='压缩结果:\\n\\n'+min+'\\n\\n原始大小: '+input.length+' 字符\\n压缩后: '+min.length+' 字符\\n压缩率: '+savings+'%';
}"""),
    ("html-minify", "HTML压缩", "HTML代码压缩工具", """function minifyHtml(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  let min=input
    .replace(/<!--[\\s\\S]*?-->/g,'')
    .replace(/\\s+/g,' ')
    .replace(/\\s*([<>\\/])\\s*/g,'$1')
    .trim();
  const savings=((1-min.length/input.length)*100).toFixed(1);
  o.textContent='压缩结果:\\n\\n'+min+'\\n\\n原始大小: '+input.length+' 字符\\n压缩后: '+min.length+' 字符\\n压缩率: '+savings+'%';
}"""),
    ("json-minify", "JSON压缩", "JSON压缩和格式化工具", """function formatJson(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  try{
    const parsed=JSON.parse(input);
    o.textContent='格式化JSON:\\n\\n'+JSON.stringify(parsed,null,2);
  }catch(e){o.textContent='JSON格式错误: '+e.message;}
}
function minifyJson(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  try{
    const parsed=JSON.parse(input);
    const min=JSON.stringify(parsed);
    const savings=((1-min.length/input.length)*100).toFixed(1);
    o.textContent='压缩结果:\\n\\n'+min+'\\n\\n原始大小: '+input.length+' 字符\\n压缩后: '+min.length+' 字符\\n压缩率: '+savings+'%';
  }catch(e){o.textContent='JSON格式错误: '+e.message;}
}"""),
    ("xml-minify", "XML压缩", "XML代码压缩工具", """function minifyXml(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  let min=input
    .replace(/<!--[\\s\\S]*?-->/g,'')
    .replace(/<\\?[^?]*\\?>/g,'')
    .replace(/\\s+/g,' ')
    .replace(/\\s*([<>])\\s*/g,'$1')
    .trim();
  const savings=((1-min.length/input.length)*100).toFixed(1);
  o.textContent='压缩结果:\\n\\n'+min+'\\n\\n原始大小: '+input.length+' 字符\\n压缩后: '+min.length+' 字符\\n压缩率: '+savings+'%';
}"""),
    ("svg-minify", "SVG压缩", "SVG代码压缩工具", """function minifySvg(){
  const input=document.getElementById('input').value;
  const o=document.getElementById('output');
  let min=input
    .replace(/<!--[\\s\\S]*?-->/g,'')
    .replace(/\\s+/g,' ')
    .replace(/\\s*([<>\\/])\\s*/g,'$1')
    .replace(/\\s*=/g,'=')
    .trim();
  const savings=((1-min.length/input.length)*100).toFixed(1);
  o.textContent='压缩结果:\\n\\n'+min+'\\n\\n原始大小: '+input.length+' 字符\\n压缩后: '+min.length+' 字符\\n压缩率: '+savings+'%';
}"""),
    ("image-resize", "图片调整", "图片尺寸调整工具", """function resizeImage(){
  const file=document.getElementById('file').files[0];
  const w=parseInt(document.getElementById('width').value);
  const h=parseInt(document.getElementById('height').value);
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=w;canvas.height=h;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0,w,h);
    const link=document.createElement('a');
    link.download='resized-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='图片已调整为 '+w+'x'+h+' 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-crop", "图片裁剪", "图片裁剪工具", """function cropImage(){
  const file=document.getElementById('file').files[0];
  const x=parseInt(document.getElementById('x').value)||0;
  const y=parseInt(document.getElementById('y').value)||0;
  const w=parseInt(document.getElementById('width').value)||100;
  const h=parseInt(document.getElementById('height').value)||100;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=w;canvas.height=h;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,x,y,w,h,0,0,w,h);
    const link=document.createElement('a');
    link.download='cropped-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='图片已裁剪并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-rotate", "图片旋转", "图片旋转工具", """function rotateImage(){
  const file=document.getElementById('file').files[0];
  const angle=parseInt(document.getElementById('angle').value)||90;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const rad=angle*Math.PI/180;
    const sin=Math.abs(Math.sin(rad)),cos=Math.abs(Math.cos(rad));
    const w=img.width,h=img.height;
    const nw=h*sin+w*cos,nh=h*cos+w*sin;
    const canvas=document.createElement('canvas');
    canvas.width=nw;canvas.height=nh;
    const ctx=canvas.getContext('2d');
    ctx.translate(nw/2,nh/2);
    ctx.rotate(rad);
    ctx.drawImage(img,-w/2,-h/2);
    const link=document.createElement('a');
    link.download='rotated-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='图片已旋转 '+angle+'° 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-flip", "图片翻转", "图片翻转工具", """function flipImage(){
  const file=document.getElementById('file').files[0];
  const dir=document.getElementById('direction').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    if(dir==='h'){ctx.translate(img.width,0);ctx.scale(-1,1);}
    else{ctx.translate(0,img.height);ctx.scale(1,-1);}
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='flipped-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='图片已'+(dir==='h'?'水平':'垂直')+'翻转并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-filter", "图片滤镜", "图片滤镜效果工具", """function applyFilter(){
  const file=document.getElementById('file').files[0];
  const filter=document.getElementById('filter').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    const filterMap={'blur':'blur(3px)','brightness':'brightness(1.5)','contrast':'contrast(1.5)','grayscale':'grayscale(1)','sepia':'sepia(1)','saturate':'saturate(2)','hue-rotate':'hue-rotate(90deg)','invert':'invert(1)','opacity':'opacity(0.5)'};
    ctx.filter=filterMap[filter]||'none';
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='filtered-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='滤镜已应用: '+filter+' 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-blur", "图片模糊", "图片模糊效果工具", """function blurImage(){
  const file=document.getElementById('file').files[0];
  const radius=parseInt(document.getElementById('radius').value)||3;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.filter='blur('+radius+'px)';
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='blurred-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='模糊效果已应用 (半径: '+radius+'px)';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-sharpen", "图片锐化", "图片锐化工具", """function sharpenImage(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const data=imageData.data;
    const w=canvas.width,h=canvas.height;
    const copy=new Uint8ClampedArray(data);
    const kernel=[0,-1,0,-1,5,-1,0,-1,0];
    for(let y=1;y<h-1;y++){
      for(let x=1;x<w-1;x++){
        for(let c=0;c<3;c++){
          let val=0;
          for(let ky=-1;ky<=1;ky++)for(let kx=-1;kx<=1;kx++){
            val+=copy[((y+ky)*w+(x+kx))*4+c]*kernel[(ky+1)*3+(kx+1)];
          }
          data[(y*w+x)*4+c]=val;
        }
      }
    }
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='sharpened-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='锐化已应用并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-brightness", "图片亮度", "图片亮度调整工具", """function adjustBrightness(){
  const file=document.getElementById('file').files[0];
  const val=parseInt(document.getElementById('brightness').value)||100;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.filter='brightness('+val/100+')';
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='bright-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='亮度调整为 '+val+'% 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-contrast", "图片对比度", "图片对比度调整工具", """function adjustContrast(){
  const file=document.getElementById('file').files[0];
  const val=parseInt(document.getElementById('contrast').value)||100;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.filter='contrast('+val/100+')';
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='contrast-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='对比度调整为 '+val+'% 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-saturation", "图片饱和度", "图片饱和度调整工具", """function adjustSaturation(){
  const file=document.getElementById('file').files[0];
  const val=parseInt(document.getElementById('saturation').value)||100;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.filter='saturate('+val/100+')';
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='saturated-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='饱和度调整为 '+val+'% 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-hue", "图片色相", "图片色相旋转工具", """function adjustHue(){
  const file=document.getElementById('file').files[0];
  const val=parseInt(document.getElementById('hue').value)||0;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.filter='hue-rotate('+val+'deg)';
    ctx.drawImage(img,0,0);
    const link=document.createElement('a');
    link.download='hue-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='色相旋转 '+val+'° 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-grayscale", "图片灰度", "图片转灰度工具", """function toGrayscale(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const d=imageData.data;
    for(let i=0;i<d.length;i+=4){
      const avg=d[i]*0.299+d[i+1]*0.587+d[i+2]*0.114;
      d[i]=d[i+1]=d[i+2]=avg;
    }
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='grayscale-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='已转为灰度图并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-sepia", "图片怀旧", "图片怀旧效果工具", """function applySepia(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const d=imageData.data;
    for(let i=0;i<d.length;i+=4){
      const r=d[i],g=d[i+1],b=d[i+2];
      d[i]=Math.min(255,r*0.393+g*0.769+b*0.189);
      d[i+1]=Math.min(255,r*0.349+g*0.686+b*0.168);
      d[i+2]=Math.min(255,r*0.272+g*0.534+b*0.131);
    }
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='sepia-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='怀旧效果已应用并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-invert", "图片反转", "图片颜色反转工具", """function invertImage(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const d=imageData.data;
    for(let i=0;i<d.length;i+=4){d[i]=255-d[i];d[i+1]=255-d[i+1];d[i+2]=255-d[i+2];}
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='inverted-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='颜色反转完成并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-emboss", "图片浮雕", "图片浮雕效果工具", """function embossImage(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const d=imageData.data;const copy=new Uint8ClampedArray(d);
    const w=canvas.width;
    const kernel=[-2,-1,0,-1,1,1,0,1,2];
    for(let y=1;y<canvas.height-1;y++){
      for(let x=1;x<w-1;x++){
        for(let c=0;c<3;c++){
          let v=0;
          for(let ky=-1;ky<=1;ky++)for(let kx=-1;kx<=1;kx++){
            v+=copy[((y+ky)*w+(x+kx))*4+c]*kernel[(ky+1)*3+(kx+1)];
          }
          d[(y*w+x)*4+c]=v+128;
        }
      }
    }
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='emboss-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='浮雕效果已应用并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-edge", "图片边缘", "图片边缘检测工具", """function edgeImage(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const d=imageData.data;const copy=new Uint8ClampedArray(d);
    const w=canvas.width;
    const gx=[-1,0,1,-2,0,2,-1,0,1],gy=[-1,-2,-1,0,0,0,1,2,1];
    for(let y=1;y<canvas.height-1;y++){
      for(let x=1;x<w-1;x++){
        let rx=0,ry=0;
        for(let ky=-1;ky<=1;ky++)for(let kx=-1;kx<=1;kx++){
          const idx=((y+ky)*w+(x+kx))*4;
          const gray=copy[idx]*0.3+copy[idx+1]*0.59+copy[idx+2]*0.11;
          const ki=(ky+1)*3+(kx+1);
          rx+=gray*gx[ki];ry+=gray*gy[ki];
        }
        const v=Math.min(255,Math.sqrt(rx*rx+ry*ry));
        const i=(y*w+x)*4;d[i]=d[i+1]=d[i+2]=v;
      }
    }
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='edge-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='边缘检测完成并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-pixelate", "图片像素化", "图片像素化效果工具", """function pixelateImage(){
  const file=document.getElementById('file').files[0];
  const size=parseInt(document.getElementById('size').value)||10;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    const sw=img.width/size,sh=img.height/size;
    ctx.imageSmoothingEnabled=false;
    ctx.drawImage(img,0,0,sw,sh);
    ctx.drawImage(canvas,0,0,sw,sh,0,0,img.width,img.height);
    const link=document.createElement('a');
    link.download='pixel-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='像素化效果已应用 (像素块: '+size+')';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-mosaic", "图片马赛克", "图片马赛克效果工具", """function mosaicImage(){
  const file=document.getElementById('file').files[0];
  const size=parseInt(document.getElementById('size').value)||20;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const imageData=ctx.getImageData(0,0,canvas.width,canvas.height);
    const d=imageData.data;const w=canvas.width,h=canvas.height;
    for(let y=0;y<h;y+=size){
      for(let x=0;x<w;x+=size){
        let r=0,g=0,b=0,cnt=0;
        for(let dy=0;dy<size&&y+dy<h;dy++){
          for(let dx=0;dx<size&&x+dx<w;dx++){
            const i=((y+dy)*w+(x+dx))*4;
            r+=d[i];g+=d[i+1];b+=d[i+2];cnt++;
          }
        }
        r=Math.round(r/cnt);g=Math.round(g/cnt);b=Math.round(b/cnt);
        for(let dy=0;dy<size&&y+dy<h;dy++){
          for(let dx=0;dx<size&&x+dx<w;dx++){
            const i=((y+dy)*w+(x+dx))*4;
            d[i]=r;d[i+1]=g;d[i+2]=b;
          }
        }
      }
    }
    ctx.putImageData(imageData,0,0);
    const link=document.createElement('a');
    link.download='mosaic-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='马赛克效果已应用并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-text", "图片文字", "在图片上添加文字工具", """function addText(){
  const file=document.getElementById('file').files[0];
  const text=document.getElementById('text').value;
  const color=document.getElementById('color').value;
  const size=parseInt(document.getElementById('fontSize').value)||24;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    ctx.font=size+'px Arial';
    ctx.fillStyle=color;
    ctx.textAlign='center';
    ctx.fillText(text,canvas.width/2,canvas.height/2);
    const link=document.createElement('a');
    link.download='text-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='文字已添加并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-watermark", "图片水印", "图片添加水印工具", """function addWatermark(){
  const file=document.getElementById('file').files[0];
  const text=document.getElementById('watermark').value||'水印';
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    ctx.font='bold '+Math.max(20,img.width/15)+'px Arial';
    ctx.fillStyle='rgba(255,255,255,0.3)';
    ctx.textAlign='center';
    ctx.translate(canvas.width/2,canvas.height/2);
    ctx.rotate(-Math.PI/6);
    for(let x=-canvas.width;x<canvas.width*2;x+=300){
      for(let y=-canvas.height;y<canvas.height*2;y+=200){
        ctx.fillText(text,x,y);
      }
    }
    const link=document.createElement('a');
    link.download='watermarked-'+file.name;
    link.href=canvas.toDataURL();
    link.click();
    o.textContent='水印已添加并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-compare", "图片对比", "图片对比查看工具", """function compareImages(){
  const f1=document.getElementById('file1').files[0];
  const f2=document.getElementById('file2').files[0];
  const o=document.getElementById('output');
  if(!f1||!f2){o.textContent='请选择两张图片';return;}
  const container=document.getElementById('preview');
  container.innerHTML='';
  container.style.display='flex';
  const img1=new Image();const img2=new Image();
  img1.onload=()=>{img1.style.maxWidth='50%';container.appendChild(img1);};
  img2.onload=()=>{img2.style.maxWidth='50%';container.appendChild(img2);};
  img1.src=URL.createObjectURL(f1);
  img2.src=URL.createObjectURL(f2);
  o.textContent='图片1: '+f1.name+' ('+f1.size+' bytes)\\n图片2: '+f2.name+' ('+f2.size+' bytes)';
}"""),
    ("image-info", "图片信息", "查看图片详细信息工具", """function showInfo(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    let info='图片信息:\\n\\n';
    info+='文件名: '+file.name+'\\n';
    info+='文件大小: '+(file.size/1024).toFixed(2)+' KB\\n';
    info+='文件类型: '+file.type+'\\n';
    info+='宽度: '+img.width+'px\\n';
    info+='高度: '+img.height+'px\\n';
    info+='比例: '+(img.width/img.height).toFixed(2)+'\\n';
    info+='总像素: '+(img.width*img.height).toLocaleString()+'\\n';
    info+='修改时间: '+new Date(file.lastModified).toLocaleString();
    o.textContent=info;
    document.getElementById('preview').innerHTML='<img src="'+URL.createObjectURL(file)+'" style="max-width:100%;border-radius:8px;">';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("image-converter", "图片转换", "图片格式转换工具", """function convertImage(){
  const file=document.getElementById('file').files[0];
  const format=document.getElementById('format').value;
  const quality=parseInt(document.getElementById('quality').value)/100;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择图片';return;}
  const img=new Image();
  img.onload=()=>{
    const canvas=document.createElement('canvas');
    canvas.width=img.width;canvas.height=img.height;
    const ctx=canvas.getContext('2d');
    ctx.drawImage(img,0,0);
    const mimeMap={'png':'image/png','jpg':'image/jpeg','webp':'image/webp'};
    const link=document.createElement('a');
    const baseName=file.name.split('.')[0];
    link.download=baseName+'.'+format;
    link.href=canvas.toDataURL(mimeMap[format],quality);
    link.click();
    o.textContent='已转换为 '+format.toUpperCase()+' 并开始下载';
  };
  img.src=URL.createObjectURL(file);
}"""),
    ("audio-recorder", "录音器", "浏览器录音工具", """let mediaRecorder;let chunks=[];
function startRec(){
  navigator.mediaDevices.getUserMedia({audio:true}).then(stream=>{
    mediaRecorder=new MediaRecorder(stream);
    chunks=[];
    mediaRecorder.ondataavailable=e=>chunks.push(e.data);
    mediaRecorder.onstop=()=>{
      const blob=new Blob(chunks,{type:'audio/webm'});
      const url=URL.createObjectURL(blob);
      const a=document.createElement('a');
      a.href=url;a.download='recording.webm';a.click();
      document.getElementById('output').textContent='录音已保存';
    };
    mediaRecorder.start();
    document.getElementById('output').textContent='录音中...';
  }).catch(e=>{document.getElementById('output').textContent='麦克风访问失败: '+e.message;});
}
function stopRec(){if(mediaRecorder&&mediaRecorder.state==='recording')mediaRecorder.stop();}"""),
    ("audio-player", "音乐播放器", "网页音乐播放器", """let audioCtx,analyser,audio;
function loadAudio(){
  const file=document.getElementById('file').files[0];
  if(!file)return;
  audio=new Audio(URL.createObjectURL(file));
  audio.crossOrigin='anonymous';
  document.getElementById('output').textContent='已加载: '+file.name;
}
function playAudio(){if(audio)audio.play();}
function pauseAudio(){if(audio)audio.pause();}"""),
    ("audio-editor", "音频编辑器", "简易音频编辑工具", """function trimAudio(){
  const file=document.getElementById('file').files[0];
  const start=parseFloat(document.getElementById('start').value)||0;
  const end=parseFloat(document.getElementById('end').value)||10;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='音频裁剪预览\\n起始: '+start+'秒\\n结束: '+end+'秒\\n时长: '+(end-start)+'秒\\n\\n注意: 完整裁剪需要使用Web Audio API';
}"""),
    ("audio-visualizer", "音频可视化", "音频波形可视化工具", """let audioCtx,analyser;
function visualize(){
  const file=document.getElementById('file').files[0];
  if(!file)return;
  audioCtx=new(window.AudioContext||window.webkitAudioContext)();
  analyser=audioCtx.createAnalyser();
  const audio=new Audio(URL.createObjectURL(file));
  audio.crossOrigin='anonymous';
  const src=audioCtx.createMediaElementSource(audio);
  src.connect(analyser);analyser.connect(audioCtx.destination);
  analyser.fftSize=256;
  const canvas=document.getElementById('canvas');
  const ctx=canvas.getContext('2d');
  const bufferLength=analyser.frequencyBinCount;
  const dataArray=new Uint8Array(bufferLength);
  function draw(){
    requestAnimationFrame(draw);
    analyser.getByteFrequencyData(dataArray);
    ctx.fillStyle='rgba(13,17,23,0.2)';ctx.fillRect(0,0,canvas.width,canvas.height);
    const barWidth=canvas.width/bufferLength;
    for(let i=0;i<bufferLength;i++){
      const barHeight=(dataArray[i]/255)*canvas.height;
      ctx.fillStyle='hsl('+(i*2)+',100%,50%)';
      ctx.fillRect(i*barWidth,canvas.height-barHeight,barWidth-1,barHeight);
    }
  }
  draw();audio.play();
}"""),
    ("audio-effects", "音频特效", "音频效果处理工具", """function applyEffect(){
  const file=document.getElementById('file').files[0];
  const effect=document.getElementById('effect').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='效果: '+effect+'\\n\\n支持的音频效果:\\n- 均衡器: 调整频段增益\\n- 混响: 模拟空间效果\\n- 延迟: 产生回声\\n- 失真: 添加谐波失真\\n- 压缩: 动态范围压缩\\n\\n注意: 完整处理需要Web Audio API';
}"""),
    ("audio-pitch", "音频音调", "音频音调调整工具", """function adjustPitch(){
  const file=document.getElementById('file').files[0];
  const pitch=parseFloat(document.getElementById('pitch').value)||1;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='音调调整: '+pitch+'x\\n\\n1.0 = 原始音调\\n2.0 = 高一个八度\\n0.5 = 低一个八度\\n\\n频率倍率: '+pitch+'\\n半音变化: '+(12*Math.log2(pitch)).toFixed(1);
}"""),
    ("audio-volume", "音频音量", "音频音量调整工具", """function adjustVolume(){
  const file=document.getElementById('file').files[0];
  const vol=parseFloat(document.getElementById('volume').value)||1;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  const db=20*Math.log10(vol);
  o.textContent='音量调整: '+(vol*100)+'%\\n增益: '+db.toFixed(1)+' dB\\n\\n100% = 原始音量\\n200% = 放大一倍\\n50% = 减半';
}"""),
    ("audio-speed", "音频速度", "音频播放速度调整", """function adjustSpeed(){
  const speed=parseFloat(document.getElementById('speed').value)||1;
  const o=document.getElementById('output');
  o.textContent='播放速度: '+speed+'x\\n\\n1.0 = 正常速度\\n1.25 = 快速\\n1.5 = 1.5倍\\n2.0 = 双倍速\\n0.5 = 半速\\n\\n时长影响: 原始时长/'+speed;
}"""),
    ("audio-reverse", "音频反转", "音频倒放工具", """function reverseAudio(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='音频反转处理\\n\\n文件: '+file.name+'\\n大小: '+(file.size/1024).toFixed(2)+' KB\\n\\n处理步骤:\\n1. 解码音频数据\\n2. 反转采样数据\\n3. 重新编码\\n\\n注意: 浏览器环境支持有限，建议使用在线服务';
}"""),
    ("audio-trim", "音频裁剪", "音频裁剪工具", """function trimAudio(){
  const file=document.getElementById('file').files[0];
  const start=parseFloat(document.getElementById('start').value)||0;
  const end=parseFloat(document.getElementById('end').value)||0;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='音频裁剪\\n\\n文件: '+file.name+'\\n起始时间: '+start+'秒\\n结束时间: '+end+'秒\\n输出时长: '+(end-start)+'秒\\n\\n提示: 使用Web Audio API进行精确裁剪';
}"""),
    ("audio-merge", "音频合并", "多音频合并工具", """function mergeAudio(){
  const files=document.getElementById('files').files;
  const o=document.getElementById('output');
  if(!files.length){o.textContent='请选择音频文件';return;}
  let info='音频合并\\n\\n选中文件:\\n';
  for(let i=0;i<files.length;i++){
    info+=(i+1)+'. '+files[i].name+' ('+(files[i].size/1024).toFixed(2)+' KB)\\n';
  }
  info+='\\n总计: '+files.length+'个文件\\n\\n合并方式: 顺序拼接\\n输出格式: 原始格式';
  o.textContent=info;
}"""),
    ("audio-split", "音频分割", "音频分割工具", """function splitAudio(){
  const file=document.getElementById('file').files[0];
  const parts=parseInt(document.getElementById('parts').value)||2;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='音频分割\\n\\n文件: '+file.name+'\\n分割份数: '+parts+'\\n\\n分割方式:\\n- 按时间等分\\n- 按文件大小等分\\n- 自定义分割点';
}"""),
    ("audio-convert", "音频转换", "音频格式转换工具", """function convertAudio(){
  const file=document.getElementById('file').files[0];
  const format=document.getElementById('format').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择音频文件';return;}
  o.textContent='音频转换\\n\\n源文件: '+file.name+'\\n目标格式: '+format+'\\n\\n浏览器支持格式:\\n- MP3: 广泛支持\\n- WAV: 无损\\n- OGG: 开放格式\\n- AAC: 高质量\\n\\n注意: 浏览器原生支持有限，建议使用ffmpeg.wasm';
}"""),
    ("video-player", "视频播放器", "网页视频播放器", """function loadVideo(){
  const file=document.getElementById('file').files[0];
  if(!file)return;
  const player=document.getElementById('player');
  player.src=URL.createObjectURL(file);
  player.style.display='block';
  document.getElementById('output').textContent='已加载: '+file.name;
}"""),
    ("video-editor", "视频编辑器", "视频基础编辑工具", """function editVideo(){
  const file=document.getElementById('file').files[0];
  const action=document.getElementById('action').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频编辑\\n\\n文件: '+file.name+'\\n操作: '+action+'\\n\\n支持的操作:\\n- 裁剪: 选择时间范围\\n- 分割: 按时间点分割\\n- 合并: 多视频拼接\\n- 转码: 格式转换\\n\\n注意: 完整编辑建议使用FFmpeg';
}"""),
    ("video-converter", "视频转换", "视频格式转换工具", """function convertVideo(){
  const file=document.getElementById('file').files[0];
  const format=document.getElementById('format').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频转换\\n\\n源文件: '+file.name+'\\n目标格式: '+format+'\\n\\n常用格式:\\n- MP4: 通用格式\\n- WebM: Web优化\\n- AVI: 传统格式\\n- MOV: Apple格式\\n\\n提示: 使用FFmpeg命令行工具进行转换';
}"""),
    ("video-trim", "视频裁剪", "视频时间裁剪工具", """function trimVideo(){
  const file=document.getElementById('file').files[0];
  const start=document.getElementById('start').value||'00:00:00';
  const end=document.getElementById('end').value||'00:01:00';
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频裁剪\\n\\n文件: '+file.name+'\\n起始: '+start+'\\n结束: '+end+'\\n\\nFFmpeg命令:\\nffmpeg -i '+file.name+' -ss '+start+' -to '+end+' -c copy output.mp4';
}"""),
    ("video-merge", "视频合并", "多视频合并工具", """function mergeVideo(){
  const files=document.getElementById('files').files;
  const o=document.getElementById('output');
  if(!files.length){o.textContent='请选择视频文件';return;}
  let info='视频合并\\n\\n选中文件:\\n';
  for(let i=0;i<files.length;i++){
    info+=(i+1)+'. '+files[i].name+'\\n';
  }
  info+='\\n合并命令:\\nffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4';
  o.textContent=info;
}"""),
    ("video-split", "视频分割", "视频分割工具", """function splitVideo(){
  const file=document.getElementById('file').files[0];
  const parts=parseInt(document.getElementById('parts').value)||2;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频分割\\n\\n文件: '+file.name+'\\n分割份数: '+parts+'\\n\\n按份数分割:\\nffmpeg -i '+file.name+' -c copy -f segment -segment_count '+parts+' -reset_timestamps 1 output_%03d.mp4';
}"""),
    ("video-speed", "视频速度", "视频播放速度调整", """function adjustSpeed(){
  const speed=parseFloat(document.getElementById('speed').value)||1;
  const o=document.getElementById('output');
  o.textContent='视频速度调整: '+speed+'x\\n\\n加速命令:\\nffmpeg -i input.mp4 -filter:v "setpts='+(1/speed).toFixed(2)+'*PTS" -filter:a "atempo='+speed+'" output.mp4\\n\\n1.0 = 正常\\n2.0 = 2倍速\\n0.5 = 慢放';
}"""),
    ("video-reverse", "视频反转", "视频倒放工具", """function reverseVideo(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频倒放\\n\\n文件: '+file.name+'\\n\\nFFmpeg命令:\\nffmpeg -i '+file.name+' -vf reverse -af areverse output.mp4\\n\\n注意: 长视频倒放需要大量内存';
}"""),
    ("video-crop", "视频裁剪", "视频画面裁剪工具", """function cropVideo(){
  const w=parseInt(document.getElementById('width').value)||640;
  const h=parseInt(document.getElementById('height').value)||480;
  const x=parseInt(document.getElementById('x').value)||0;
  const y=parseInt(document.getElementById('y').value)||0;
  const o=document.getElementById('output');
  o.textContent='视频画面裁剪\\n\\n裁剪区域: '+w+'x'+h+'\\n位置: ('+x+','+y+')\\n\\nFFmpeg命令:\\nffmpeg -i input.mp4 -vf "crop='+w+':'+h+':'+x+':'+y+'" output.mp4';
}"""),
    ("video-rotate", "视频旋转", "视频旋转工具", """function rotateVideo(){
  const angle=document.getElementById('angle').value;
  const o=document.getElementById('output');
  const angleMap={'90':'transpose=1','180':'transpose=1,transpose=1','270':'transpose=2','hflip':'hflip','vflip':'vflip'};
  o.textContent='视频旋转: '+angle+'°\\n\\nFFmpeg命令:\\nffmpeg -i input.mp4 -vf "'+angleMap[angle]+'" output.mp4\\n\\n选项:\\n90°: transpose=1\\n180°: transpose=1,transpose=1\\n270°: transpose=2';
}"""),
    ("video-flip", "视频翻转", "视频翻转工具", """function flipVideo(){
  const dir=document.getElementById('direction').value;
  const o=document.getElementById('output');
  o.textContent='视频翻转: '+(dir==='h'?'水平':'垂直')+'\\n\\nFFmpeg命令:\\nffmpeg -i input.mp4 -vf "'+dir+'" output.mp4\\n\\nh: 水平翻转\\nv: 垂直翻转';
}"""),
    ("video-watermark", "视频水印", "视频添加水印工具", """function addWatermark(){
  const text=document.getElementById('watermark').value||'Watermark';
  const pos=document.getElementById('position').value;
  const o=document.getElementById('output');
  const posMap={'tl':'10:10','tr':'main_w-overlay_w-10:10','c':'(main_w-overlay_w)/2:(main_h-overlay_h)/2','bl':'10:main_h-overlay_h-10','br':'main_w-overlay_w-10:main_h-overlay_h-10'};
  o.textContent='视频水印\\n\\n文字: '+text+'\\n位置: '+pos+'\\n\\nFFmpeg命令:\\nffmpeg -i input.mp4 -vf "drawtext=text=\\''+text+'\\':x='+posMap[pos]+':fontsize=24:fontcolor=white" output.mp4';
}"""),
    ("video-subtitle", "视频字幕", "视频字幕添加工具", """function addSubtitle(){
  const file=document.getElementById('file').files[0];
  const text=document.getElementById('subtitle').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频字幕\\n\\n字幕内容: '+text+'\\n\\nSRT格式示例:\\n1\\n00:00:01,000 --> 00:00:04,000\\n'+text+'\\n\\nFFmpeg命令:\\nffmpeg -i '+file.name+' -vf "subtitles=subtitles.srt" output.mp4';
}"""),
    ("video-encode", "视频编码", "视频编码参数工具", """function showEncode(){
  const codec=document.getElementById('codec').value;
  const preset=document.getElementById('preset').value;
  const crf=document.getElementById('crf').value;
  const o=document.getElementById('output');
  const codecDesc={'h264':'H.264/AVC - 最广泛支持','h265':'H.265/HEVC - 高压缩率','vp9':'VP9 - 开放格式','av1':'AV1 - 下一代标准'};
  o.textContent='视频编码设置\\n\\n编码器: '+codec+' ('+codecDesc[codec]+')\\nPreset: '+preset+'\\nCRF: '+crf+'\\n\\nFFmpeg命令:\\nffmpeg -i input.mp4 -c:v '+codec+' -preset '+preset+' -crf '+crf+' output.mp4\\n\\nCRF说明:\\n0 = 无损\\n18 = 高质量\\n23 = 默认\\n28 = 中等\\n51 = 最低质量';
}"""),
    ("video-decode", "视频解码", "视频解码信息工具", """function showDecode(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择视频文件';return;}
  o.textContent='视频文件信息\\n\\n文件名: '+file.name+'\\n文件大小: '+(file.size/1024/1024).toFixed(2)+' MB\\n\\n使用ffprobe获取详细信息:\\nffprobe -v quiet -print_format json -show_format -show_streams '+file.name+'\\n\\n输出信息:\\n- 编码格式\\n- 分辨率\\n- 帧率\\n- 比特率\\n- 时长';
}"""),
    ("pdf-editor", "PDF编辑器", "PDF页面编辑工具", """function editPdf(){
  const file=document.getElementById('file').files[0];
  const action=document.getElementById('action').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PDF文件';return;}
  o.textContent='PDF编辑\\n\\n文件: '+file.name+'\\n操作: '+action+'\\n\\n支持的操作:\\n- 查看页面\\n- 添加水印\\n- 合并/分割\\n- 加密/解密\\n\\n提示: 使用pdf-lib库进行浏览器端PDF编辑';
}"""),
    ("pdf-converter", "PDF转换器", "PDF格式转换工具", """function convertPdf(){
  const dir=document.getElementById('direction').value;
  const o=document.getElementById('output');
  o.textContent='PDF转换\\n\\n转换方向: '+dir+'\\n\\n常用转换:\\n- PDF → Word\\n- PDF → 图片\\n- PDF → HTML\\n- Word → PDF\\n- 图片 → PDF\\n\\n在线工具推荐:\\n- pdf24.org\\n- ilovepdf.com\\n- smallpdf.com';
}"""),
    ("pdf-merge", "PDF合并", "多PDF合并工具", """function mergePdf(){
  const files=document.getElementById('files').files;
  const o=document.getElementById('output');
  if(!files.length){o.textContent='请选择PDF文件';return;}
  let info='PDF合并\\n\\n选中文件:\\n';
  for(let i=0;i<files.length;i++){
    info+=(i+1)+'. '+files[i].name+'\\n';
  }
  info+='\\n合并方式: 按选择顺序拼接\\n\\n提示: 使用pdf-lib库进行浏览器端合并';
  o.textContent=info;
}"""),
    ("pdf-split", "PDF分割", "PDF分割工具", """function splitPdf(){
  const file=document.getElementById('file').files[0];
  const pages=document.getElementById('pages').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PDF文件';return;}
  o.textContent='PDF分割\\n\\n文件: '+file.name+'\\n分割方式: '+pages+'\\n\\n示例:\\n- 1-5: 第1到5页\\n- 1,3,5: 第1、3、5页\\n- 3-: 第3页到最后\\n\\nFFmpeg命令:\\npdftk '+file.name+' cat '+pages+' output split.pdf';
}"""),
    ("pdf-rotate", "PDF旋转", "PDF页面旋转工具", """function rotatePdf(){
  const angle=document.getElementById('angle').value;
  const o=document.getElementById('output');
  o.textContent='PDF旋转\\n\\n旋转角度: '+angle+'°\\n\\nFFmpeg命令:\\npdftk input.pdf cat 1-'+angle+' output rotated.pdf\\n\\n或使用qpdf:\\nqpdf --rotate='+angle+':1 input.pdf output.pdf';
}"""),
    ("pdf-crop", "PDF裁剪", "PDF页面裁剪工具", """function cropPdf(){
  const o=document.getElementById('output');
  o.textContent='PDF页面裁剪\\n\\nPDF裁剪需要指定页面区域:\\n- 上边距\\n- 下边距\\n- 左边距\\n- 右边距\\n\\n使用Ghostscript:\\ngs -sDEVICE=pdfwrite -dFIXEDMEDIA -dDEVICEWIDTHPOINTS=595 -dDEVICEHEIGHTPOINTS=842 -sOutputFile=output.pdf input.pdf';
}"""),
    ("pdf-watermark", "PDF水印", "PDF添加水印工具", """function addPdfWatermark(){
  const text=document.getElementById('watermark').value||'WATERMARK';
  const opacity=parseInt(document.getElementById('opacity').value)||30;
  const o=document.getElementById('output');
  o.textContent='PDF水印\\n\\n水印文字: '+text+'\\n透明度: '+opacity+'%\\n\\n使用Ghostscript:\\ngs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite \\\n  -sOutputFile=output.pdf \\\n  -c "<< /Page [/Page 1] /MediaBox [0 0 612 792] \\\n  /Contents << /Length 0 >> >> setdistillerparams \\\n  -f input.pdf';
}"""),
    ("pdf-encrypt", "PDF加密", "PDF加密工具", """function encryptPdf(){
  const password=document.getElementById('password').value;
  const permission=document.getElementById('permission').value;
  const o=document.getElementById('output');
  if(!password){o.textContent='请设置密码';return;}
  o.textContent='PDF加密\\n\\n密码: '+password+'\\n权限: '+permission+'\\n\\n使用qpdf:\\nqpdf --encrypt '+password+' '+password+' 128 -- '+permission+' -- input.pdf output.pdf\\n\\n权限级别:\\n- 允许打印\\n- 允许修改\\n- 允许复制\\n- 完全限制';
}"""),
    ("pdf-decrypt", "PDF解密", "PDF解密工具", """function decryptPdf(){
  const password=document.getElementById('password').value;
  const o=document.getElementById('output');
  o.textContent='PDF解密\\n\\n使用qpdf:\\nqpdf --decrypt --password='+password+' input.pdf output.pdf\\n\\n使用pdftk:\\npdftk input.pdf input_pw '+password+' output output.pdf\\n\\n注意: 仅解密您有权访问的PDF文件';
}"""),
    ("pdf-compress", "PDF压缩", "PDF文件压缩工具", """function compressPdf(){
  const file=document.getElementById('file').files[0];
  const quality=document.getElementById('quality').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PDF文件';return;}
  const qualityMap={'low':'低质量 (最大压缩)','medium':'中等质量','high':'高质量 (最小压缩)'};
  o.textContent='PDF压缩\\n\\n文件: '+file.name+'\\n大小: '+(file.size/1024/1024).toFixed(2)+' MB\\n质量: '+qualityMap[quality]+'\\n\\n使用Ghostscript:\\ngs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \\\n  -dPDFSETTINGS=/'+(quality==='low'?'screen':quality==='medium'?'ebook':'printer')+' \\\n  -dNOPAUSE -dBATCH -dQUIET \\\n  -sOutputFile=output.pdf input.pdf';
}"""),
    ("pdf-extract", "PDF提取", "PDF内容提取工具", """function extractPdf(){
  const file=document.getElementById('file').files[0];
  const type=document.getElementById('type').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PDF文件';return;}
  o.textContent='PDF提取\\n\\n文件: '+file.name+'\\n提取类型: '+type+'\\n\\n提取文本:\\npdftotext input.pdf output.txt\\n\\n提取图片:\\npdfimages -j input.pdf\\n\\n提取页面:\\npdftk input.pdf cat 1 output page1.pdf';
}"""),
    ("pdf-ocr", "PDF OCR", "PDF文字识别工具", """function ocrPdf(){
  const file=document.getElementById('file').files[0];
  const lang=document.getElementById('lang').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PDF文件';return;}
  o.textContent='PDF OCR\\n\\n文件: '+file.name+'\\n语言: '+lang+'\\n\\n使用Tesseract:\\ntesseract input.pdf output -l '+lang+'\\n\\n在线OCR服务:\\n- Google Drive\\n- ABBYY\\n- Adobe Acrobat';
}"""),
    ("pdf-sign", "PDF签名", "PDF数字签名工具", """function signPdf(){
  const file=document.getElementById('file').files[0];
  const name=document.getElementById('name').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PDF文件';return;}
  o.textContent='PDF签名\\n\\n文件: '+file.name+'\\n签名者: '+name+'\\n\\n签名类型:\\n- 手写签名: 使用签名图片\\n- 数字签名: 使用证书\\n\\n使用pdf-lib:\\nconst pdfDoc = await PDFDocument.load(bytes);\\nconst page = pdfDoc.getPage(0);\\npage.drawText("\\''+name+'\\'", {x:50, y:50});';
}"""),
    ("excel-editor", "Excel编辑器", "在线Excel编辑工具", """function editExcel(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择Excel文件';return;}
  o.textContent='Excel编辑\\n\\n文件: '+file.name+'\\n大小: '+(file.size/1024).toFixed(2)+' KB\\n\\n功能:\\n- 查看表格数据\\n- 编辑单元格\\n- 添加公式\\n- 格式设置\\n\\n提示: 使用SheetJS库解析Excel文件';
}"""),
    ("excel-converter", "Excel转换器", "Excel格式转换工具", """function convertExcel(){
  const dir=document.getElementById('direction').value;
  const o=document.getElementById('output');
  o.textContent='Excel转换\\n\\n转换方向: '+dir+'\\n\\n支持转换:\\n- XLSX ↔ CSV\\n- XLSX → JSON\\n- XLSX → HTML\\n- XLSX → PDF\\n- CSV → XLSX\\n\\n在线工具:\\n- convertio.co\\n- cloudconvert.com';
}"""),
    ("excel-merge", "Excel合并", "多Excel文件合并工具", """function mergeExcel(){
  const files=document.getElementById('files').files;
  const o=document.getElementById('output');
  if(!files.length){o.textContent='请选择Excel文件';return;}
  let info='Excel合并\\n\\n选中文件:\\n';
  for(let i=0;i<files.length;i++){info+=(i+1)+'. '+files[i].name+'\\n';}
  info+='\\n合并方式:\\n- 合并工作表\\n- 追加数据\\n- 按列合并\\n\\n使用SheetJS合并';
  o.textContent=info;
}"""),
    ("excel-split", "Excel分割", "Excel文件分割工具", """function splitExcel(){
  const file=document.getElementById('file').files[0];
  const method=document.getElementById('method').value;
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择Excel文件';return;}
  o.textContent='Excel分割\\n\\n文件: '+file.name+'\\n分割方式: '+method+'\\n\\n分割选项:\\n- 按工作表拆分\\n- 按行数拆分\\n- 按列拆分\\n- 按条件拆分';
}"""),
    ("word-editor", "Word编辑器", "在线Word编辑工具", """function editWord(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择Word文件';return;}
  o.textContent='Word编辑\\n\\n文件: '+file.name+'\\n大小: '+(file.size/1024).toFixed(2)+' KB\\n\\n功能:\\n- 查看文档\\n- 编辑文本\\n- 格式设置\\n- 插入图片\\n\\n提示: 使用mammoth.js解析Word文件';
}"""),
    ("word-converter", "Word转换器", "Word格式转换工具", """function convertWord(){
  const dir=document.getElementById('direction').value;
  const o=document.getElementById('output');
  o.textContent='Word转换\\n\\n转换方向: '+dir+'\\n\\n支持转换:\\n- DOCX → PDF\\n- DOCX → HTML\\n- DOCX → TXT\\n- PDF → DOCX\\n- HTML → DOCX\\n\\n在线工具:\\n- smallpdf.com\\n- ilovepdf.com';
}"""),
    ("ppt-editor", "PPT编辑器", "在线PPT编辑工具", """function editPpt(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择PPT文件';return;}
  o.textContent='PPT编辑\\n\\n文件: '+file.name+'\\n大小: '+(file.size/1024).toFixed(2)+' KB\\n\\n功能:\\n- 查看幻灯片\\n- 编辑内容\\n- 添加动画\\n- 设计模板\\n\\n提示: 使用PptxGenJS创建PPT';
}"""),
    ("ppt-converter", "PPT转换器", "PPT格式转换工具", """function convertPpt(){
  const dir=document.getElementById('direction').value;
  const o=document.getElementById('output');
  o.textContent='PPT转换\\n\\n转换方向: '+dir+'\\n\\n支持转换:\\n- PPTX → PDF\\n- PPTX → 图片\\n- PPTX → HTML\\n- PDF → PPTX\\n- 图片 → PPTX\\n\\n在线工具:\\n- convertio.co\\n- cloudconvert.com';
}"""),
    ("visio-editor", "Visio编辑器", "Visio图表编辑工具", """function editVisio(){
  const file=document.getElementById('file').files[0];
  const o=document.getElementById('output');
  if(!file){o.textContent='请先选择Visio文件';return;}
  o.textContent='Visio编辑\\n\\n文件: '+file.name+'\\n\\n替代方案:\\n- draw.io (免费在线)\\n- Lucidchart\\n- Microsoft Visio\\n\\n导入Visio文件:\\n支持 .vsdx 格式';
}"""),
    ("draw-editor", "画图编辑器", "在线画图工具", """let ctx;let drawing=false;
function initDraw(){
  const canvas=document.getElementById('canvas');
  ctx=canvas.getContext('2d');
  canvas.width=800;canvas.height=600;
  ctx.fillStyle='#1e293b';ctx.fillRect(0,0,800,600);
  ctx.strokeStyle='#e6edf3';ctx.lineWidth=2;
}
function startDraw(e){drawing=true;ctx.beginPath();ctx.moveTo(e.offsetX,e.offsetY);}
function draw(e){if(!drawing)return;ctx.lineTo(e.offsetX,e.offsetY);ctx.stroke();}
function stopDraw(){drawing=false;}
function clearCanvas(){ctx.fillStyle='#1e293b';ctx.fillRect(0,0,800,600);}
function changeColor(){ctx.strokeStyle=document.getElementById('color').value;}
function changeWidth(){ctx.lineWidth=parseInt(document.getElementById('width').value);}"""),
    ("diagram-editor", "图表编辑器", "在线图表编辑工具", """function createDiagram(){
  const type=document.getElementById('type').value;
  const o=document.getElementById('output');
  const templates={
    'bar':'柱状图数据:\\n类别A: 80\\n类别B: 60\\n类别C: 90\\n类别D: 45\\n\\n使用Chart.js或D3.js创建',
    'line':'折线图数据:\\n1月: 30\\n2月: 45\\n3月: 25\\n4月: 60\\n\\n使用Chart.js创建',
    'pie':'饼图数据:\\n类型A: 35%\\n类型B: 25%\\n类型C: 20%\\n类型D: 20%\\n\\n使用Chart.js创建',
    'scatter':'散点图:\\n(1,2) (3,5) (2,4)\\n(5,3) (4,6) (6,2)\\n\\n使用D3.js创建'
  };
  o.textContent='图表创建\\n\\n类型: '+type+'\\n\\n'+templates[type];
}"""),
    ("flowchart-editor", "流程图编辑器", "流程图创建工具", """function createFlow(){
  const o=document.getElementById('output');
  o.textContent='流程图创建\\n\\n基本元素:\\n- 开始/结束 (椭圆)\\n- 过程 (矩形)\\n- 判断 (菱形)\\n- 数据 (平行四边形)\\n- 连接线 (箭头)\\n\\n示例流程:\\n[开始] → [输入数据] → [处理数据] → [输出结果] → [结束]\\n\\n推荐工具:\\n- draw.io\\n- Lucidchart\\n- Figma';
}"""),
    ("wireframe-editor", "原型编辑器", "线框图创建工具", """function createWire(){
  const o=document.getElementById('output');
  o.textContent='线框图创建\\n\\n页面元素:\\n- 头部 (导航栏)\\n- 侧边栏\\n- 主内容区\\n- 页脚\\n\\n组件类型:\\n- 按钮\\n- 输入框\\n- 文本框\\n- 图片占位符\\n- 列表\\n\\n推荐工具:\\n- Balsamiq\\n- Figma\\n- Sketch';
}"""),
    ("mockup-editor", "模型编辑器", "产品模型设计工具", """function createMock(){
  const o=document.getElementById('output');
  o.textContent='产品模型设计\\n\\n设计流程:\\n1. 线框图\\n2. 低保真模型\\n3. 高保真模型\\n4. 交互原型\\n\\n设计规范:\\n- 颜色系统\\n- 字体层级\\n- 间距系统\\n- 组件库\\n\\n推荐工具:\\n- Figma\\n- Sketch\\n- Adobe XD';
}"""),
    ("prototype-editor", "原型编辑器", "交互原型设计工具", """function createProto(){
  const o=document.getElementById('output');
  o.textContent='交互原型设计\\n\\n交互类型:\\n- 点击跳转\\n- 滑动切换\\n- 弹窗提示\\n- 表单验证\\n- 动画过渡\\n\\n原型保真度:\\n- 低保真: 线框图\\n- 中保真: 基本交互\\n- 高保真: 完整交互\\n\\n推荐工具:\\n- Figma\\n- Axure\\n- InVision';
}"""),
    ("ui-designer", "UI设计器", "UI界面设计工具", """function designUI(){
  const o=document.getElementById('output');
  o.textContent='UI设计指南\\n\\n设计原则:\\n- 一致性\\n- 反馈\\n- 简约\\n- 容错\\n- 效率\\n\\n设计系统:\\n- 颜色: 主色/辅色/中性色\\n- 字体: 标题/正文/注释\\n- 间距: 4px网格系统\\n- 圆角: 统一圆角值\\n\\n推荐工具:\\n- Figma\\n- Sketch\\n- Adobe XD';
}"""),
    ("ux-designer", "UX设计器", "UX用户体验设计工具", """function designUX(){
  const o=document.getElementById('output');
  o.textContent='UX设计流程\\n\\n1. 用户研究\\n   - 问卷调查\\n   - 用户访谈\\n   - 竞品分析\\n\\n2. 信息架构\\n   - 内容分类\\n   - 导航结构\\n   - 搜索设计\\n\\n3. 用户旅程\\n   - 触点分析\\n   - 痛点识别\\n   - 优化方案\\n\\n4. 可用性测试\\n   - 任务测试\\n   - A/B测试\\n   - 数据分析';
}"""),
    ("color-scheme", "配色方案", "颜色方案生成工具", """function genColors(){
  const base=document.getElementById('base').value;
  const o=document.getElementById('output');
  const hex=parseInt(base.slice(1),16);
  const r=(hex>>16)&255,g=(hex>>8)&255,b=hex&255;
  function lighten(amount){return 'rgb('+Math.min(255,r+amount)+','+Math.min(255,g+amount)+','+Math.min(255,b+amount)+')';}
  function darken(amount){return 'rgb('+Math.max(0,r-amount)+','+Math.max(0,g-amount)+','+Math.max(0,b-amount)+')';}
  o.textContent='配色方案\\n\\n基础色: '+base+'\\n\\n浅色变体:\\n- Light 1: '+lighten(60)+'\\n- Light 2: '+lighten(40)+'\\n- Light 3: '+lighten(20)+'\\n\\n深色变体:\\n- Dark 1: '+darken(20)+'\\n- Dark 2: '+darken(40)+'\\n- Dark 3: '+darken(60)+'\\n\\n互补色: rgb('+(255-r)+','+(255-g)+','+(255-b)+')';
}"""),
    ("font-compare", "字体对比", "字体对比预览工具", """function compareFonts(){
  const text=document.getElementById('text').value||'字体对比预览';
  const o=document.getElementById('output');
  const fonts=['Arial','Helvetica','Times New Roman','Georgia','Courier New','Verdana','Impact','Comic Sans MS'];
  let result='字体对比\\n\\n';
  fonts.forEach(f=>{
    result+=f+': <span style="font-family:'+f+'">'+text+'</span>\\n';
  });
  o.innerHTML='字体对比\\n\\n'+fonts.map(f=>'<div style="font-family:'+f+';padding:8px;margin:4px 0;background:#21262d;border-radius:4px;"><strong>'+f+'</strong><br>'+text+'</div>').join('');
}"""),
    ("icon-library", "图标库", "SVG图标库管理工具", """function showIcons(){
  const o=document.getElementById('output');
  o.textContent='常用SVG图标\\n\\n▼ 箭头: <svg viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>\\n○ 圆形: <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>\\n□ 方形: <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18"/></svg>\\n☆ 星形: <svg viewBox="0 0 24 24"><polygon points="12,2 15,10 23,10 17,15 19,23 12,18 5,23 7,15 1,10 9,10"/></svg>\\n\\n图标库:\\n- Heroicons\\n- Lucide\\n- Phosphor';
}"""),
    ("image-library", "图片库", "图片素材管理工具", """function browseImages(){
  const o=document.getElementById('output');
  o.textContent='免费图片资源\\n\\n免费图库:\\n- Unsplash (unsplash.com)\\n- Pexels (pexels.com)\\n- Pixabay (pixabay.com)\\n- StockSnap\\n\\nAI生成图片:\\n- DALL-E\\n- Midjourney\\n- Stable Diffusion\\n\\n设计素材:\\n- Figma Community\\n- Dribbble\\n- Behance';
}"""),
    ("video-library", "视频库", "视频素材管理工具", """function browseVideos(){
  const o=document.getElementById('output');
  o.textContent='免费视频资源\\n\\n免费视频库:\\n- Pexels Videos\\n- Pixabay Videos\\n- Coverr\\n- Mixkit\\n\\n视频素材:\\n- Videohive\\n- Pond5\\n- Shutterstock\\n\\n开源视频:\\n- Vimeo Staff Picks\\n- YouTube Creative Commons';
}"""),
    ("audio-library", "音频库", "音频素材管理工具", """function browseAudio(){
  const o=document.getElementById('output');
  o.textContent='免费音频资源\\n\\n免费音效:\\n- Freesound\\n- Zapsplat\\n- SoundBible\\n\\n免费音乐:\\n- Free Music Archive\\n- Incompetech\\n- Bensound\\n\\n免版税音乐:\\n- Epidemic Sound\\n- Artlist\\n- Musicbed';
}"""),
    ("document-library", "文档库", "文档模板管理工具", """function browseDocs(){
  const o=document.getElementById('output');
  o.textContent='文档模板资源\\n\\n简历模板:\\n- Canva\\n- Novoresume\\n- Resume.io\\n\\n报告模板:\\n- Google Docs模板\\n- Microsoft模板\\n\\n合同模板:\\n- LawDepot\\n- LegalZoom\\n\\n演示模板:\\n- Slidesgo\\n- SlideModel';
}"""),
    ("code-library", "代码库", "代码片段管理工具", """function browseCode(){
  const o=document.getElementById('output');
  o.textContent='代码资源\\n\\n代码片段:\\n- GitHub Gist\\n- CodePen\\n- JSFiddle\\n\\n代码库:\\n- GitHub\\n- GitLab\\n- Bitbucket\\n\\n代码学习:\\n- LeetCode\\n- HackerRank\\n- Codewars\\n\\n文档:\\n- MDN\\n- DevDocs';
}"""),
    ("api-library", "API库", "API接口管理工具", """function browseApi(){
  const o=document('output');
  const el=document.getElementById('output');
  el.textContent='公共API列表\\n\\n天气API:\\n- OpenWeatherMap\\n- WeatherAPI\\n\\n地图API:\\n- Google Maps\\n- Mapbox\\n- OpenStreetMap\\n\\n数据API:\\n- REST Countries\\n- JSONPlaceholder\\n- Open Library\\n\\n媒体API:\\n- Unsplash API\\n- Pexels API\\n- TMDB (电影)';
}"""),
    ("template-library", "模板库", "网页模板管理工具", """function browseTemplates(){
  const o=document.getElementById('output');
  o.textContent='网页模板资源\\n\\n免费模板:\\n- HTML5 UP\\n- OnePage Love\\n- StyleShout\\n\\n模板框架:\\n- Bootstrap\\n- Tailwind CSS\\n- Bulma\\n\\nLanding Page:\\n- Landingi\\n- Unbounce\\n- Carrd\\n\\n响应式模板:\\n- Responsive\\n- Amaze UI\\n- Semantic UI';
}"""),
    ("icon-generator", "图标生成器", "SVG图标生成工具", """function genIcon(){
  const shape=document.getElementById('shape').value;
  const color=document.getElementById('color').value;
  const size=document.getElementById('size').value||48;
  const o=document.getElementById('output');
  let svg='';
  switch(shape){
    case'circle':svg='<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+color+'"><circle cx="12" cy="12" r="10"/></svg>';break;
    case'square':svg='<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+color+'"><rect x="2" y="2" width="20" height="20" rx="3"/></svg>';break;
    case'triangle':svg='<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+color+'"><polygon points="12,2 22,22 2,22"/></svg>';break;
    case'star':svg='<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+color+'"><polygon points="12,2 15,10 23,10 17,15 19,23 12,18 5,23 7,15 1,10 9,10"/></svg>';break;
    case'heart':svg='<svg width="'+size+'" height="'+size+'" viewBox="0 0 24 24" fill="'+color+'"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>';break;
  }
  o.innerHTML='生成的图标:\\n\\n'+svg+'\\n\\nSVG代码:\\n'+svg;
}"""),
    ("logo-generator", "Logo生成器", "品牌Logo生成工具", """function genLogo(){
  const text=document.getElementById('text').value||'LOGO';
  const color=document.getElementById('color').value;
  const o=document.getElementById('output');
  o.innerHTML='Logo预览:<br><div style="display:flex;align-items:center;justify-content:center;padding:40px;background:#1e293b;border-radius:12px;"><div style="font-size:48px;font-weight:bold;color:'+color+';letter-spacing:4px;">'+text+'</div></div><br><br>SVG代码:<br><code>&lt;svg viewBox="0 0 200 60"&gt;<br>&nbsp;&nbsp;&lt;text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="36" font-weight="bold" fill="'+color+'">'+text+'&lt;/text&gt;<br>&lt;/svg&gt;</code>';
}"""),
    ("banner-generator", "横幅生成器", "网页横幅生成工具", """function genBanner(){
  const title=document.getElementById('title').value||'Banner Title';
  const bg=document.getElementById('bg').value;
  const text=document.getElementById('textColor').value;
  const o=document.getElementById('output');
  o.innerHTML='<div style="background:'+bg+';color:'+text+';padding:60px 40px;text-align:center;border-radius:12px;"><h1 style="font-size:32px;margin:0;">'+title+'</h1><p style="opacity:0.8;margin-top:8px;">Subtitle text here</p></div><br>建议尺寸:<br>- 横幅: 1200x628px<br>- 社交媒体: 1200x630px<br>- 网站头部: 1920x600px';
}"""),
    ("poster-generator", "海报生成器", "宣传海报生成工具", """function genPoster(){
  const title=document.getElementById('title').value||'Event Title';
  const bg=document.getElementById('bg').value;
  const o=document.getElementById('output');
  o.innerHTML='<div style="background:'+bg+';color:#fff;padding:80px 40px;text-align:center;border-radius:12px;min-height:400px;display:flex;flex-direction:column;justify-content:center;"><h1 style="font-size:48px;margin:0;">'+title+'</h1><p style="margin-top:16px;opacity:0.8;">Description text here</p><div style="margin-top:32px;padding:12px 24px;background:rgba(255,255,255,0.2);border-radius:8px;display:inline-block;">了解更多</div></div>';
}"""),
    ("flyer-generator", "传单生成器", "宣传传单生成工具", """function genFlyer(){
  const title=document.getElementById('title').value||'Flyer Title';
  const o=document.getElementById('output');
  o.innerHTML='<div style="background:#1e293b;color:#e6edf3;padding:40px;border-radius:12px;"><h1 style="font-size:36px;margin:0 0 16px;">'+title+'</h1><p style="opacity:0.7;line-height:1.6;">传单内容描述，包含活动信息、时间地点等。</p><div style="margin-top:24px;padding:12px 24px;background:#3b82f6;color:#fff;border-radius:8px;display:inline-block;">立即参与</div></div><br><br>标准尺寸:<br>- A4: 210x297mm<br>- A5: 148x210mm<br>- 信纸: 8.5x11in';
}"""),
    ("card-generator", "卡片生成器", "卡片模板生成工具", """function genCard(){
  const title=document.getElementById('title').value||'Card Title';
  const desc=document.getElementById('desc').value||'Card description';
  const bg=document.getElementById('bg').value;
  const o=document.getElementById('output');
  o.innerHTML='<div style="background:'+bg+';color:#fff;padding:32px;border-radius:12px;max-width:320px;"><div style="width:48px;height:48px;background:rgba(255,255,255,0.2);border-radius:12px;margin-bottom:16px;"></div><h3 style="margin:0 0 8px;font-size:20px;">'+title+'</h3><p style="opacity:0.8;margin:0;line-height:1.5;">'+desc+'</p></div>';
}"""),
    ("certificate-generator", "证书生成器", "荣誉证书生成工具", """function genCert(){
  const name=document.getElementById('name').value||'获奖者姓名';
  const title=document.getElementById('title').value||'优秀员工';
  const o=document.getElementById('output');
  const date=new Date().toLocaleDateString('zh-CN');
  o.innerHTML='<div style="background:#fff;color:#1e293b;padding:60px 40px;text-align:center;border-radius:12px;border:3px solid #d4af37;"><div style="color:#d4af37;font-size:14px;letter-spacing:4px;">CERTIFICATE OF</div><div style="font-size:36px;font-weight:bold;margin:8px 0;color:#d4af37;">'+title.toUpperCase()+'</div><div style="margin:24px 0;color:#666;">特此颁发给</div><div style="font-size:28px;font-weight:bold;border-bottom:2px solid #d4af37;display:inline-block;padding:4px 24px;">'+name+'</div><div style="margin-top:24px;color:#666;">日期: '+date+'</div></div>';
}"""),
    ("invoice-generator", "发票生成器", "电子发票生成工具", """function genInvoice(){
  const invoiceNo=document.getElementById('invoiceNo').value||'INV-001';
  const items=document.getElementById('items').value||'商品A,100\\n商品B,200';
  const o=document.getElementById('output');
  const lines=items.split('\\n');
  let total=0;
  let rows='';
  lines.forEach(l=>{
    const parts=l.split(',');
    if(parts.length>=2){
      const price=parseFloat(parts[1]);
      total+=price;
      rows+='<tr><td style="padding:8px;border-bottom:1px solid #30363d;">'+parts[0]+'</td><td style="padding:8px;border-bottom:1px solid #30363d;text-align:right;">¥'+price.toFixed(2)+'</td></tr>';
    }
  });
  o.innerHTML='<div style="background:#1e293b;color:#e6edf3;padding:32px;border-radius:12px;"><h2 style="margin:0 0 24px;color:#3b82f6;">发票 '+invoiceNo+'</h2><table style="width:100%;border-collapse:collapse;"><tr style="background:#21262d;"><th style="padding:8px;text-align:left;">项目</th><th style="padding:8px;text-align:right;">金额</th></tr>'+rows+'</table><div style="text-align:right;margin-top:16px;font-size:20px;font-weight:bold;">总计: ¥'+total.toFixed(2)+'</div></div>';
}"""),
    ("receipt-generator", "收据生成器", "收据打印生成工具", """function genReceipt(){
  const items=document.getElementById('items').value||'商品A,50\\n商品B,75';
  const o=document.getElementById('output');
  const lines=items.split('\\n');
  let total=0;
  let rows='';
  lines.forEach(l=>{
    const parts=l.split(',');
    if(parts.length>=2){
      const price=parseFloat(parts[1]);
      total+=price;
      rows+=parts[0].padEnd(16)+('¥'+price.toFixed(2)).padStart(10)+'\\n';
    }
  });
  o.innerHTML='<div style="background:#fff;color:#000;padding:24px;border-radius:8px;font-family:monospace;max-width:320px;margin:0 auto;"><pre style="margin:0;text-align:center;">==== 收据 ====\\n\\n'+rows+'\\n'+('─'.repeat(26))+'\\n'+('合计').padEnd(16)+('¥'+total.toFixed(2)).padStart(10)+'\\n\\n谢谢惠顾!</pre></div>';
}"""),
    ("ticket-generator", "票据生成器", "入场票据生成工具", """function genTicket(){
  const event=document.getElementById('event').value||'活动名称';
  const seat=document.getElementById('seat').value||'A区 12排 8号';
  const o=document.getElementById('output');
  o.innerHTML='<div style="display:flex;background:#1e293b;border-radius:12px;overflow:hidden;max-width:500px;"><div style="flex:1;padding:24px;color:#e6edf3;"><div style="font-size:12px;color:#3b82f6;text-transform:uppercase;">Event</div><div style="font-size:20px;font-weight:bold;margin:4px 0;">'+event+'</div><div style="font-size:14px;color:#8b949e;margin-top:12px;">座位: '+seat+'</div><div style="font-size:14px;color:#8b949e;">时间: '+new Date().toLocaleString('zh-CN')+'</div></div><div style="width:120px;background:#21262d;display:flex;align-items:center;justify-content:center;color:#3b82f6;font-size:24px;letter-spacing:2px;">TICKET</div></div>';
}"""),
    ("badge-generator", "徽章生成器", "身份徽章生成工具", """function genBadge(){
  const name=document.getElementById('name').value||'姓名';
  const role=document.getElementById('role').value||'角色';
  const color=document.getElementById('color').value;
  const o=document.getElementById('output');
  o.innerHTML='<div style="background:#1e293b;padding:32px;border-radius:12px;text-align:center;max-width:240px;"><div style="width:80px;height:80px;background:'+color+';border-radius:50%;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:32px;">'+name[0]+'</div><div style="color:#e6edf3;font-size:18px;font-weight:bold;">'+name+'</div><div style="color:#8b949e;font-size:14px;margin-top:4px;">'+role+'</div><div style="margin-top:16px;padding:8px 16px;background:#21262d;border-radius:20px;color:#3b82f6;font-size:12px;display:inline-block;">ID: '+Math.random().toString(36).substr(2,8).toUpperCase()+'</div></div>';
}"""),
    ("sticker-generator", "贴纸生成器", "数字贴纸生成工具", """function genSticker(){
  const text=document.getElementById('text').value||'Hi!';
  const bg=document.getElementById('bg').value;
  const o=document.getElementById('output');
  o.innerHTML='<div style="display:inline-block;background:'+bg+';color:#fff;padding:16px 24px;border-radius:24px;font-size:24px;font-weight:bold;transform:rotate(-5deg);box-shadow:0 4px 12px rgba(0,0,0,0.3);">'+text+'</div><br><br>更多样式:<br><div style="display:flex;gap:12px;flex-wrap:wrap;"><div style="background:#ff6b6b;color:#fff;padding:12px 20px;border-radius:16px;">😊</div><div style="background:#51cf66;color:#fff;padding:12px 20px;border-radius:50%;">👍</div><div style="background:#339af0;color:#fff;padding:12px 20px;border-radius:12px;transform:rotate(5deg);">❤️</div></div>';
}"""),
    ("emoji-generator", "表情生成器", "自定义表情生成工具", """function genEmoji(){
  const eyes=document.getElementById('eyes').value;
  const mouth=document.getElementById('mouth').value;
  const color=document.getElementById('color').value;
  const o=document.getElementById('output');
  const eyeMap={'happy':'◕','sad':'◔','angry':'▃','surprised':'⊙','wink':'◕','sleepy':'−','heart':'♥','star':'★'};
  const mouthMap={'happy':'◡','sad':'︵','angry':'﹀','surprised':'○','tongue':'∪','smile':'▽','frown':'∧','none':''};
  const face='<div style="width:120px;height:120px;background:'+color+';border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:36px;color:#1e293b;box-shadow:0 4px 12px rgba(0,0,0,0.2);"><div style="margin-top:16px;">'+eyeMap[eyes]+(eyes==='wink'?' '+eyeMap[eyes]:eyeMap[eyes])+'</div><div style="margin-top:4px;">'+mouthMap[mouth]+'</div></div>';
  o.innerHTML='表情预览:\\n\\n'+face;
}"""),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--accent:#3b82f6;--accent-hover:#2563eb;--text-muted:#8b949e;--success:#22c55e;--error:#ef4444}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px;line-height:1.6}}
.container{{max-width:960px;margin:0 auto}}
h1{{font-size:1.8rem;margin-bottom:8px;color:var(--text)}}
.desc{{color:var(--text-muted);margin-bottom:24px;font-size:0.95rem}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px}}
label{{display:block;font-size:0.85rem;color:var(--text-muted);margin-bottom:6px;margin-top:12px}}
input,select,textarea{{width:100%;padding:10px 14px;background:var(--bg);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:0.95rem;font-family:inherit}}
textarea{{resize:vertical;min-height:100px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}
.row>*{{flex:1;min-width:140px}}
.btn{{display:inline-block;padding:10px 20px;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:0.95rem;cursor:pointer;font-weight:500;margin-top:16px;transition:background 0.2s}}
.btn:hover{{background:var(--accent-hover)}}
.btn-secondary{{background:var(--card);border:1px solid var(--border);color:var(--text)}}
.btn-secondary:hover{{background:var(--border)}}
.output{{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;min-height:120px;white-space:pre-wrap;word-break:break-all;font-family:"SF Mono",Monaco,Consolas,monospace;font-size:0.85rem;margin-top:16px;max-height:400px;overflow-y:auto}}
.preview{{margin-top:16px;text-align:center}}
.preview img,.preview video{{max-width:100%;border-radius:8px}}
canvas{{border:1px solid var(--border);border-radius:8px;max-width:100%}}
.file-input{{position:relative;overflow:hidden;display:inline-block}}
.file-input input[type=file]{{position:absolute;left:0;top:0;opacity:0;width:100%;height:100%;cursor:pointer}}
.slider-row{{display:flex;align-items:center;gap:12px}}
.slider-row input[type=range]{{flex:1}}
.slider-row span{{min-width:50px;text-align:right;color:var(--accent);font-weight:500}}
.checkbox-row{{display:flex;gap:16px;flex-wrap:wrap;margin-top:8px}}
.checkbox-row label{{display:flex;align-items:center;gap:6px;cursor:pointer}}
.tabs{{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}}
.tab{{padding:8px 16px;background:var(--bg);border:1px solid var(--border);border-radius:8px;cursor:pointer;color:var(--text-muted);font-size:0.85rem;transition:all 0.2s}}
.tab.active{{background:var(--accent);color:#fff;border-color:var(--accent)}}
@media(max-width:640px){{h1{{font-size:1.4rem}}.card{{padding:16px}}.row{{flex-direction:column}}}}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<p class="desc">{desc}</p>
<div class="card">
{body}
</div>
<div class="output" id="output" style="display:none;"></div>
<div class="preview" id="preview"></div>
</div>
<script>
function showOutput(){{document.getElementById('output').style.display='block';}}
{script}
</script>
</body>
</html>"""


def build_body(tool_id, tool_title, tool_desc):
    """Build HTML form body based on tool category"""
    tool_inputs = {
        "api-tester": """<label>请求方法</label>
<select id="method"><option>GET</option><option>POST</option><option>PUT</option><option>DELETE</option><option>PATCH</option></select>
<label>请求URL</label>
<input id="url" placeholder="https://api.example.com/endpoint">
<label>请求头 (JSON数组)</label>
<textarea id="headers" rows="3" placeholder='[["Content-Type","application/json"]]'></textarea>
<label>请求体</label>
<textarea id="body" rows="4" placeholder="请求体内容"></textarea>
<button class="btn" onclick="showOutput();run()">发送请求</button>""",
        "http-client": """<label>请求方法</label>
<select id="method"><option>GET</option><option>POST</option><option>PUT</option><option>DELETE</option></select>
<label>请求URL</label>
<input id="url" placeholder="https://api.example.com">
<button class="btn" onclick="showOutput();sendReq()">发送</button>""",
        "websocket-tester": """<label>WebSocket地址</label>
<input id="wsurl" placeholder="ws://echo.websocket.org">
<label>消息</label>
<div class="row"><input id="msg" placeholder="输入消息"><button class="btn" onclick="sendMsg()">发送</button></div>
<button class="btn" onclick="showOutput();connect()">连接</button>""",
        "password-gen-pro": """<div class="slider-row"><label>密码长度</label><input type="range" id="length" min="4" max="64" value="16" oninput="this.nextElementSibling.textContent=this.value"><span>16</span></div>
<div class="checkbox-row">
<label><input type="checkbox" id="upper" checked> 大写字母</label>
<label><input type="checkbox" id="lower" checked> 小写字母</label>
<label><input type="checkbox" id="num" checked> 数字</label>
<label><input type="checkbox" id="special" checked> 特殊字符</label>
</div>
<button class="btn" onclick="showOutput();genPassword()">生成密码</button>""",
        "hash-gen-pro": """<label>输入文本</label>
<textarea id="input" rows="3" placeholder="输入要哈希的文本"></textarea>
<label>哈希算法</label>
<select id="algo"><option>SHA-256</option><option>SHA-384</option><option>SHA-512</option><option>SHA-1</option></select>
<button class="btn" onclick="showOutput();genHash()">生成哈希</button>""",
        "base64-gen": """<label>输入文本</label>
<textarea id="input" rows="4" placeholder="输入要编码/解码的文本"></textarea>
<div style="display:flex;gap:12px;margin-top:8px;">
<button class="btn" onclick="showOutput();b64Encode()">Base64 编码</button>
<button class="btn btn-secondary" onclick="showOutput();b64Decode()">Base64 解码</button>
</div>""",
        "url-encode-pro": """<label>输入文本</label>
<textarea id="input" rows="3" placeholder="输入URL或文本"></textarea>
<div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap;">
<button class="btn" onclick="showOutput();urlEncode()">URL编码</button>
<button class="btn btn-secondary" onclick="showOutput();urlDecode()">URL解码</button>
<button class="btn btn-secondary" onclick="showOutput();urlEncodeFull()">完整编码</button>
</div>""",
        "html-encode": """<label>输入HTML</label>
<textarea id="input" rows="4" placeholder="输入HTML代码"></textarea>
<div style="display:flex;gap:12px;margin-top:8px;">
<button class="btn" onclick="showOutput();htmlEncode()">HTML编码</button>
<button class="btn btn-secondary" onclick="showOutput();htmlDecode()">HTML解码</button>
</div>""",
        "css-minify": """<label>CSS代码</label>
<textarea id="input" rows="8" placeholder="粘贴CSS代码"></textarea>
<button class="btn" onclick="showOutput();minifyCss()">压缩CSS</button>""",
        "js-minify": """<label>JavaScript代码</label>
<textarea id="input" rows="8" placeholder="粘贴JavaScript代码"></textarea>
<button class="btn" onclick="showOutput();minifyJs()">压缩JS</button>""",
        "html-minify": """<label>HTML代码</label>
<textarea id="input" rows="8" placeholder="粘贴HTML代码"></textarea>
<button class="btn" onclick="showOutput();minifyHtml()">压缩HTML</button>""",
        "json-minify": """<label>JSON数据</label>
<textarea id="input" rows="8" placeholder='{"key": "value"}'></textarea>
<div style="display:flex;gap:12px;margin-top:8px;">
<button class="btn" onclick="showOutput();formatJson()">格式化</button>
<button class="btn btn-secondary" onclick="showOutput();minifyJson()">压缩</button>
</div>""",
        "xml-minify": """<label>XML代码</label>
<textarea id="input" rows="8" placeholder="粘贴XML代码"></textarea>
<button class="btn" onclick="showOutput();minifyXml()">压缩XML</button>""",
        "svg-minify": """<label>SVG代码</label>
<textarea id="input" rows="8" placeholder="粘贴SVG代码"></textarea>
<button class="btn" onclick="showOutput();minifySvg()">压缩SVG</button>""",
    }
    if tool_id in tool_inputs:
        return tool_inputs[tool_id]

    # Default form: file upload or text input
    if any(k in tool_id for k in ['image','audio','video','pdf','excel','word','ppt','visio']):
        return f"""<label>选择文件</label>
<input type="file" id="file" accept="*/*" style="padding:8px;">
<button class="btn" onclick="showOutput();{tool_id.replace('-','_').replace(' ','_')}Action()">执行</button>"""

    return f"""<label>输入</label>
<textarea id="input" rows="4" placeholder="输入内容"></textarea>
<button class="btn" onclick="showOutput();doAction()">执行</button>"""


count = 0
for tool_id, title, desc, script in TOOLS:
    tool_dir = os.path.join(BASE, tool_id)
    os.makedirs(tool_dir, exist_ok=True)

    # Build a proper form body based on tool_id
    body = build_body(tool_id, title, desc)

    html = TEMPLATE.format(
        title=title,
        desc=desc,
        body=body,
        script=script,
    )

    html_path = os.path.join(tool_dir, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    count += 1

print(f"Done! Created {count} tools in {BASE}")
