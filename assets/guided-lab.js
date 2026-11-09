/* Shared guided workspace. Existing module storage keys and earlier responses survive revisions. */
(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("lab-data").textContent);
  const form = document.getElementById("lab-workspace");
  const status = document.getElementById("save-status");
  let work = {};
  try {
    const saved = JSON.parse(localStorage.getItem(data.key) || "{}");
    if (saved && typeof saved === "object" && !Array.isArray(saved)) work = saved;
  } catch { status.textContent = "Browser saving is unavailable. Download your work before leaving."; }
  const fields = () => [...form.querySelectorAll("input,textarea")];
  const escapeHTML = s => String(s ?? "").replace(/[&<>"']/g, c =>
    ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const problemParts = problem => [...problem.querySelectorAll("textarea[data-response]")];
  function progress() {
    const answers = [...form.querySelectorAll("textarea[data-response]")];
    const n = answers.filter(e => e.value.trim()).length;
    document.getElementById("progress").value = answers.length ? 100*n/answers.length : 0;
    document.getElementById("progress-label").textContent = n+" of "+answers.length+" parts started";
    form.querySelectorAll(".problem").forEach(p => {
      const attempted = problemParts(p).some(e => e.value.trim()) ||
        [...p.querySelectorAll(".check-row input")].some(e => e.value.trim());
      const detail=p.querySelector(".solution");
      detail.classList.toggle("locked", !attempted);
      if (!attempted) detail.open=false;
    });
  }
  function save() {
    fields().forEach(e => { work[e.id] = e.value; });
    try {
      localStorage.setItem(data.key, JSON.stringify(work));
      status.textContent = "Saved in this browser.";
    } catch {
      status.textContent = "Browser saving is unavailable. Use Prepare Submission to download your work.";
    }
    progress();
  }
  fields().forEach(e => { if (work[e.id] != null) e.value = work[e.id]; });
  data.problems.forEach((p,i) => {
    const id=data.prefix+i;
    if (!String(work[id] ?? "").trim()) return;
    const parent=document.getElementById("problem-"+(i+1));
    const details=document.createElement("details");details.className="legacy";
    const summary=document.createElement("summary");summary.textContent="Your saved response from the earlier lab";
    const label=document.createElement("label");label.htmlFor=id;label.textContent="Earlier response (kept with your submission)";
    const area=document.createElement("textarea");area.id=id;area.value=work[id];
    details.append(summary,label,area);parent.append(details);
  });
  form.addEventListener("input", save);
  form.querySelectorAll(".solution summary").forEach(s => s.addEventListener("click", e => {
    if (s.parentElement.classList.contains("locked")) {
      e.preventDefault();
      const msg=s.parentElement.querySelector(".attempt-message");
      msg.textContent="Try a part of this problem first, then open the explanation.";
      s.textContent="Try a part of this problem first";
      setTimeout(()=>{s.textContent="Compare your solution after an attempt";},2200);
    }
  }));
  function number(s) {
    const str=s.trim().replace(/,/g,"");
    if (/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(str)) return Number(str);
    const m=str.match(/^([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*\/\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))$/);
    return m && Number(m[2]) !== 0 ? Number(m[1])/Number(m[2]) : NaN;
  }
  form.querySelectorAll("[data-check]").forEach(b => b.addEventListener("click", () => {
    const input=document.getElementById(b.dataset.check);
    const value=number(input.value), target=Number(input.dataset.answer);
    const tol=Number(input.dataset.tolerance || "0.000001");
    const out=b.parentElement.querySelector(".feedback");
    const correct=Number.isFinite(value) && Math.abs(value-target)<=tol;
    out.className="feedback "+(correct?"correct":"retry");
    out.textContent=correct?"This value checks. Include your reasoning above.":
      !Number.isFinite(value)?"Enter a decimal or a fraction, such as 3/4.":
      "Check the setup, signs, and units. You can open the hint or compare the solution after an attempt.";
    input.setAttribute("aria-invalid",String(!correct));save();
  }));
  document.getElementById("clear-work").addEventListener("click", () => {
    if (!confirm("Clear this module's saved lab answers on this device?")) return;
    work={};fields().forEach(e=>e.value="");
    form.querySelectorAll(".legacy").forEach(e=>e.remove());
    form.querySelectorAll(".feedback,.attempt-message").forEach(e=>e.textContent="");
    form.querySelectorAll(".solution").forEach(e=>e.open=false);
    save();
  });
  document.getElementById("next-problem").addEventListener("click", () => {
    const problems=[...form.querySelectorAll(".problem")];
    const next=problems.find(p=>p.getBoundingClientRect().top>80) || problems[0];
    next.scrollIntoView({behavior:"smooth",block:"start"});
    next.querySelector("textarea").focus({preventScroll:true});
  });
  let previous=null;
  function submission() {
    save();
    let html='<div class="submission-actions"><button id="submission-print">Print / Save PDF</button>'+
      '<a id="submission-download" class="download-button">Download HTML</a><button class="secondary" id="return-lab">Return to Lab</button></div>'+
      '<h2>Lab submission</h2><p><strong>Student:</strong> '+escapeHTML(work.student || "(name not entered)")+
      '<br><strong>Date:</strong> '+escapeHTML(work.date || "")+'</p>';
    form.querySelectorAll(".problem").forEach(p=>{
      html+='<section class="submission-question"><h2>'+p.querySelector("h2").innerHTML+'</h2>';
      html+='<div>'+p.querySelector(".problem-context").innerHTML+'</div>';
      p.querySelectorAll(".part").forEach(part=>{
        const answer=part.querySelector("textarea");
        html+='<div class="submission-part"><strong>'+part.querySelector("label").innerHTML+'</strong>'+
          '<div class="submission-answer">'+escapeHTML(answer.value || "(no response)")+'</div>';
        const numeric=part.querySelector(".check-row input");
        if(numeric && numeric.value.trim()) html+='<p class="small">'+
          escapeHTML(part.querySelector(".check-row label").textContent)+": "+escapeHTML(numeric.value)+'</p>';
        html+='</div>';
      });
      const earlier=p.querySelector(".legacy textarea");
      if (earlier && earlier.value.trim()) html+='<h3>Earlier saved response</h3><div class="submission-answer">'+escapeHTML(earlier.value)+'</div>';
      html+='</section>';
    });
    previous=document.createDocumentFragment();
    while(form.firstChild)previous.appendChild(form.firstChild);
    const view=document.createElement("section");view.id="submission-view";view.innerHTML=html;form.append(view);
    document.body.classList.add("submission-mode");
    document.getElementById("submission-print").onclick=()=>window.print();
    function prepareDownload() {
      const clone=document.documentElement.cloneNode(true);
      clone.querySelectorAll("script, .submission-actions, .rail").forEach(e=>e.remove());
      clone.querySelectorAll('link[rel="stylesheet"]').forEach(e=>e.remove());
      const style=document.createElement("style");style.textContent=
        "body{max-width:900px;margin:30px auto;padding:20px;font:17px/1.6 Georgia,serif;color:#182b3b}"+
        ".masthead{border-bottom:1px solid #aaa}.masthead a,.module-nav,.skip,footer{display:none}"+
        ".submission-part{margin:22px 0;break-inside:avoid}.submission-answer{white-space:pre-wrap;overflow-wrap:anywhere;padding:10px 0}"+
        "h2{margin-top:32px}h2,h3{break-after:avoid}.small{font-size:14px}figure img{max-width:100%}"+
        "mjx-container{max-width:100%}";
      clone.querySelector("head").append(style);
      // MathJax SVG remains in the document; user-entered text was escaped before insertion.
      const blob=new Blob(["<!doctype html>\n"+clone.outerHTML],{type:"text/html"});
      const url=URL.createObjectURL(blob), a=document.getElementById("submission-download");
      const name=(work.student||"Student").trim().replace(/[^a-zA-Z0-9_-]+/g,"_").slice(0,60);
      a.href=url;a.download="MATH142_Module"+String(data.module).padStart(2,"0")+"_Lab_"+name+".html";
      return url;
    }
    const exportURL=prepareDownload();
    document.getElementById("return-lab").onclick=()=>{
      form.replaceChildren(previous);previous=null;document.body.classList.remove("submission-mode");
      setTimeout(()=>URL.revokeObjectURL(exportURL),3000);
      progress();if(window.MathJax?.typesetPromise)window.MathJax.typesetPromise([form]).catch(()=>{});
    };
    window.scrollTo({top:0,behavior:"smooth"});
    if(window.MathJax?.typesetPromise)window.MathJax.typesetPromise([view]).catch(()=>{});
  }
  document.getElementById("prepare-submission").addEventListener("click",submission);
  progress();
})();
