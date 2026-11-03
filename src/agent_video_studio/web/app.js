const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const translations = {
  es: {
    newProject:"Nuevo proyecto",workspace:"ESPACIO DE TRABAJO",agentReady:"Listo para agentes",agentHint:"Conecta Claude, Codex o tu modelo.",localWorkspace:"Espacio local",overview:"Overview",integrations:"Integraciones",studioLabel:"AI VIDEO WORKSPACE",welcomeTitle:"De una idea.<br><em>A un video que se mueve.</em>",welcomeDescription:"Crea desde cero o transforma tus videos largos en clips listos para compartir. Tú eliges los agentes, nosotros conectamos el flujo completo.",modeOne:"01 · CREAR",ideaToVideo:"Idea a video",ideaHint:"Guion, voz, escenas y formatos.",modeTwo:"02 · REUTILIZAR",longToClips:"Video largo a clips",longHint:"Transcripción, cortes y subtítulos.",startProject:"EMPIEZA UN PROYECTO",tellUs:"Cuéntanos qué quieres crear",projectName:"Nombre del proyecto",creativeBrief:"Brief creativo",createProject:"Crear proyecto",addSource:"Añadir video o audio",localFirst:"Local-first",providerAgnostic:"Modelos a tu elección",renderVideo:"Render video",stepCreate:"Brief",stepBuild:"Construir",stepExport:"Exportar",sourceMedia:"Material fuente",sourceMediaHint:"Añade el video o audio que quieres transformar.",optional:"OPCIONAL",dropFile:"Arrastra un archivo aquí",orBrowse:"o",browseFiles:"explora tu equipo",uploading:"Subiendo...",scriptStoryboard:"Guion y storyboard",scriptHint:"Genera escenas editables con el modelo elegido.",generateScript:"Generar guion",emptyScenes:"Las escenas aparecerán aquí cuando generes el guion o analices el material.",clipCandidates:"Momentos destacados",clipHint:"Selecciona los cortes que quieras llevar al timeline.",analyzeSource:"Analizar fuente",useClips:"Usar clips",renderedExports:"Videos exportados",exportHint:"Descarga videos, subtítulos y archivos del proyecto.",projectSettings:"Ajustes del proyecto",outputLanguage:"Idioma de salida",outputFormats:"Formatos de salida",burnCaptions:"Quemar subtítulos",burnCaptionsHint:"También exporta SRT y VTT.",voiceover:"Voz en off",voiceoverHint:"Genera narración para cada escena.",modelProvider:"Proveedor de modelo",refresh:"Actualizar",checking:"Comprobando configuración...",providerSetupNote:"Las claves se configuran localmente en el archivo .env. Nunca se muestran en la interfaz.",configureProviders:"Configurar proveedores",agentTools:"Herramientas para agentes",agentToolsHint:"Mismo proyecto. Distintas interfaces.",connectAgent:"Conectar un agente",distribution:"Distribución",distributionHint:"Exporta ahora. Conecta redes cuando quieras.",exportReady:"Export listo",setupNeeded:"Configurar",publishApproval:"Publicar requiere autorización y confirmación explícita.",connectorsLabel:"CONECTORES",connectTitle:"Tu stack creativo, conectado.",connectDescription:"Configura las claves en tu .env local y elige qué proveedores pueden procesar cada proyecto.",readSetup:"Ver guía de configuración",noProjects:"Tus proyectos aparecerán aquí",untitled:"Proyecto sin título",saved:"Guardado",draft:"Borrador",processing:"Procesando",ready:"Listo",failed:"Error",scriptGenerated:"Guion y storyboard generados.",analysisDone:"Transcripción y cortes sugeridos listos.",clipsSelected:"Cortes añadidos al timeline.",renderQueued:"Render iniciado. Puedes seguir su progreso aquí.",chooseClips:"Selecciona al menos un corte.",fileUploaded:"Archivo añadido al proyecto.",uploadError:"No se pudo subir el archivo.",genericError:"Algo salió mal. Revisa el detalle e inténtalo de nuevo.",transcript:"Transcripción",clip:"clip",clips:"clips",seconds:"s",saving:"Guardado",title:"Título",narration:"Narración",visualDirection:"Dirección visual",caption:"Subtítulo",generatedBy:"Generado por",downloadVideo:"Video MP4",downloadSrt:"Subtítulos SRT",downloadVtt:"Subtítulos VTT",downloadProject:"Proyecto",noExports:"Aún no hay videos renderizados.",waiting:"Esperando configuración",providerConfigured:"Configurado",notConfigured:"Sin configurar",jobFailed:"La tarea falló",imported:"Importado",selection:"seleccionados",createPrompt:"Describe la idea, el público, el tono y la acción final.",repurposePrompt:"Importa un video o podcast y crea cortes con marcas de tiempo.",targetDuration:"Duración objetivo",analysisNeedsProvider:"Configura proveedor de texto y transcripción en .env.",renderNeedsScene:"Genera un guion o elige cortes antes de renderizar.",formatVertical:"Vertical · 9:16",formatLandscape:"Landscape · 16:9",formatSquare:"Square · 1:1",modePromptLabel:"IDEA A VIDEO",modeRepurposeLabel:"VIDEO LARGO A CLIPS"
  },
  en: {
    newProject:"New project",workspace:"WORKSPACE",agentReady:"Agents are ready",agentHint:"Connect Claude, Codex, or your model.",localWorkspace:"Local workspace",overview:"Overview",integrations:"Integrations",studioLabel:"AI VIDEO WORKSPACE",welcomeTitle:"From an idea.<br><em>To a video that moves.</em>",welcomeDescription:"Create from scratch or turn long videos into clips ready to share. Choose your agents; the studio connects the full workflow.",modeOne:"01 · CREATE",ideaToVideo:"Idea to video",ideaHint:"Script, voice, scenes, and formats.",modeTwo:"02 · REPURPOSE",longToClips:"Long video to clips",longHint:"Transcript, cuts, and captions.",startProject:"START A PROJECT",tellUs:"Tell us what you want to create",projectName:"Project name",creativeBrief:"Creative brief",createProject:"Create project",addSource:"Add video or audio",localFirst:"Local-first",providerAgnostic:"Choose your models",renderVideo:"Render video",stepCreate:"Brief",stepBuild:"Build",stepExport:"Export",sourceMedia:"Source media",sourceMediaHint:"Add the video or audio you want to transform.",optional:"OPTIONAL",dropFile:"Drop a file here",orBrowse:"or",browseFiles:"browse your computer",uploading:"Uploading...",scriptStoryboard:"Script and storyboard",scriptHint:"Generate editable scenes with your chosen model.",generateScript:"Generate script",emptyScenes:"Scenes will appear here after you generate a script or analyze source media.",clipCandidates:"Highlights",clipHint:"Select the cuts you want to add to the timeline.",analyzeSource:"Analyze source",useClips:"Use clips",renderedExports:"Rendered videos",exportHint:"Download videos, captions, and project files.",projectSettings:"Project settings",outputLanguage:"Output language",outputFormats:"Output formats",burnCaptions:"Burn in captions",burnCaptionsHint:"SRT and VTT are exported too.",voiceover:"Voiceover",voiceoverHint:"Generate narration for each scene.",modelProvider:"Model provider",refresh:"Refresh",checking:"Checking provider setup...",providerSetupNote:"Keys are configured locally in .env and are never shown in the interface.",configureProviders:"Configure providers",agentTools:"Agent tools",agentToolsHint:"One project. Multiple interfaces.",connectAgent:"Connect an agent",distribution:"Distribution",distributionHint:"Export now. Connect social accounts when ready.",exportReady:"Export ready",setupNeeded:"Setup needed",publishApproval:"Publishing requires authorization and explicit confirmation.",connectorsLabel:"CONNECTORS",connectTitle:"Your creative stack, connected.",connectDescription:"Set keys in your local .env and choose which providers can process each project.",readSetup:"Open setup guide",noProjects:"Your projects will appear here",untitled:"Untitled project",saved:"Saved",draft:"Draft",processing:"Processing",ready:"Ready",failed:"Failed",scriptGenerated:"Script and storyboard generated.",analysisDone:"Transcript and clip suggestions are ready.",clipsSelected:"Clips added to the timeline.",renderQueued:"Render started. Progress will appear here.",chooseClips:"Select at least one clip.",fileUploaded:"File added to project.",uploadError:"Could not upload this file.",genericError:"Something went wrong. Review the detail and try again.",transcript:"Transcript",clip:"clip",clips:"clips",seconds:"s",saving:"Saved",title:"Title",narration:"Narration",visualDirection:"Visual direction",caption:"Caption",generatedBy:"Generated by",downloadVideo:"Video MP4",downloadSrt:"Captions SRT",downloadVtt:"Captions VTT",downloadProject:"Project",noExports:"No videos rendered yet.",waiting:"Waiting for setup",providerConfigured:"Configured",notConfigured:"Not configured",jobFailed:"Job failed",imported:"Imported",selection:"selected",createPrompt:"Describe the idea, audience, tone, and call to action.",repurposePrompt:"Import a video or podcast to create timestamped clips.",targetDuration:"Target duration",analysisNeedsProvider:"Configure text and transcription providers in .env.",renderNeedsScene:"Generate a script or select clips before rendering.",formatVertical:"Vertical · 9:16",formatLandscape:"Landscape · 16:9",formatSquare:"Square · 1:1",modePromptLabel:"IDEA TO VIDEO",modeRepurposeLabel:"LONG VIDEO TO CLIPS"
  }
};

Object.assign(translations.es, {
  publishLabel: "PUBLICACIÓN", publishTitle: "Revisa el post antes de enviarlo.",
  publishSubtitle: "Se enviará el video y los metadatos a la cuenta conectada.",
  destination: "Destino", postTitle: "Título", postCaption: "Descripción / caption",
  visibility: "Visibilidad", shareToFeed: "Compartir también en el feed",
  aiLabel: "Marcar como contenido generado con IA",
  confirmPublish: "Confirmo destino, video, texto y visibilidad. Publicar enviará el contenido.",
  publishNow: "Publicar ahora", publishAction: "Publicar", preflightLoading: "Comprobando requisitos…",
  preflightReady: "Listo para publicar. Revisa cada campo y confirma para enviar.",
  preflightBlocked: "Faltan requisitos para publicar:", publishSuccess: "Solicitud enviada a la plataforma.",
  private: "Privado", unlisted: "No listado", public: "Público", visibilityUnavailable: "No disponible",
  loading: "Cargando…", deliveries: "Publicaciones", published: "Publicado",
  publishedProcessing: "Procesando en la plataforma"
});
Object.assign(translations.en, {
  publishLabel: "PUBLISHING", publishTitle: "Review the post before sending it.",
  publishSubtitle: "The video and metadata will be sent to the connected account.",
  destination: "Destination", postTitle: "Title", postCaption: "Description / caption",
  visibility: "Visibility", shareToFeed: "Also share to feed",
  aiLabel: "Label this as AI-generated content",
  confirmPublish: "I confirm the destination, video, text, and visibility. Publishing sends the content.",
  publishNow: "Publish now", publishAction: "Publish", preflightLoading: "Checking requirements…",
  preflightReady: "Ready to publish. Review every field and confirm to send.",
  preflightBlocked: "Publishing requirements are missing:", publishSuccess: "Request sent to the platform.",
  private: "Private", unlisted: "Unlisted", public: "Public", visibilityUnavailable: "Not available",
  loading: "Loading…", deliveries: "Deliveries", published: "Published",
  publishedProcessing: "Processing on platform"
});

let state = { mode: "prompt", projectId: null, bundle: null, language: localStorage.getItem("avs-language") || "es", polling: false, pendingSourceFile: null, publishing: null, publishOptions: [] };

function t(key) { return translations[state.language]?.[key] || translations.es[key] || key; }
function tr(key) { return t(key); }

function applyLanguage() {
  document.documentElement.lang = state.language;
  $$("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (key === "welcomeTitle") el.innerHTML = t(key);
    else el.textContent = t(key);
  });
  $("#language-toggle").textContent = state.language.toUpperCase();
  $("#project-brief").placeholder = state.mode === "prompt" ? t("createPrompt") : t("repurposePrompt");
  $("#project-title").placeholder = state.language === "es" ? "Ej. Lanzamiento de producto" : "e.g. Product launch";
  $("#form-title").textContent = state.mode === "prompt" ? t("tellUs") : t("repurposePrompt");
  if (state.bundle) renderBundle(state.bundle);
  loadProjects();
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : null;
  if (!response.ok) throw new Error(payload?.detail || `${response.status} ${response.statusText}`);
  return payload;
}

function toast(message, error = false) {
  const element = $("#toast");
  element.textContent = message;
  element.classList.toggle("error", error);
  element.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => element.classList.remove("show"), 3000);
}

function setMode(mode) {
  state.mode = mode;
  $$(".mode-card").forEach((card) => card.classList.toggle("active", card.dataset.mode === mode));
  $("#project-brief").placeholder = t(mode === "prompt" ? "createPrompt" : "repurposePrompt");
  $("#form-title").textContent = t(mode === "prompt" ? "tellUs" : "repurposePrompt");
  $("#upload-inline").hidden = mode !== "repurpose";
}

function showWelcome() {
  state.projectId = null;
  state.bundle = null;
  $("#welcome-view").hidden = false;
  $("#project-view").hidden = true;
  $("#breadcrumb-project").textContent = t("overview");
  setMode("prompt");
}

async function loadProjects() {
  try {
    const projects = await api("/api/projects");
    $("#project-count").textContent = String(projects.length);
    const nav = $("#project-list");
    nav.replaceChildren();
    if (!projects.length) {
      const empty = document.createElement("div");
      empty.className = "sidebar-empty";
      empty.textContent = t("noProjects");
      nav.append(empty);
      return;
    }
    for (const project of projects) {
      const button = document.createElement("button");
      button.className = `project-nav-item ${state.projectId === project.id ? "active" : ""}`;
      button.innerHTML = `<span class="project-nav-icon">${project.mode === "repurpose" ? "▧" : "✳"}</span>`;
      const title = document.createElement("span");
      title.className = "project-nav-title";
      title.textContent = project.title;
      button.append(title);
      button.addEventListener("click", () => openProject(project.id));
      nav.append(button);
    }
  } catch (error) {
    console.warn("Project list unavailable", error);
  }
}

async function createProject(event) {
  event.preventDefault();
  const title = $("#project-title").value.trim();
  const brief = $("#project-brief").value.trim();
  if (!title) return;
  const button = $("#create-form button[type=submit]");
  button.disabled = true;
  try {
    const project = await api("/api/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        mode: state.mode,
        brief,
        language: $("#language-select").value,
        aspect_ratios: [$("#aspect-select").value]
      })
    });
    await openProject(project.id);
    if (state.pendingSourceFile) {
      const file = state.pendingSourceFile;
      state.pendingSourceFile = null;
      await uploadFile(file);
    }
  } catch (error) {
    toast(error.message || t("genericError"), true);
  } finally {
    button.disabled = false;
  }
}

async function openProject(projectId) {
  try {
    const bundle = await api(`/api/projects/${encodeURIComponent(projectId)}`);
    state.projectId = projectId;
    state.bundle = bundle;
    $("#welcome-view").hidden = true;
    $("#project-view").hidden = false;
    $("#breadcrumb-project").textContent = bundle.project.title;
    renderBundle(bundle);
    await loadProjects();
  } catch (error) {
    toast(error.message || t("genericError"), true);
  }
}

function renderBundle(bundle) {
  const project = bundle.project;
  $("#project-heading-title").textContent = project.title;
  const brief = project.document.brief || "";
  $("#project-heading-subtitle").textContent = brief;
  $("#project-mode-label").textContent = t(project.mode === "prompt" ? "modePromptLabel" : "modeRepurposeLabel");
  $("#project-status").textContent = t(project.status || "draft");
  $("#brief-summary").textContent = brief;
  $("#brief-summary").hidden = !brief;
  $("#project-language").value = project.document.language || "en";
  const ratios = project.document.aspect_ratios || ["9:16"];
  $$('input[name="format"]').forEach((input) => { input.checked = ratios.includes(input.value); });
  $("#highlights-card").hidden = project.mode !== "repurpose";
  renderAssets(bundle.assets || []);
  renderScenes(project.document.timeline?.scenes || []);
  renderHighlights(project.document.highlights || []);
  renderExports(project.document.exports || [], bundle.jobs || [], project.document.deliveries || []);
  renderProvider(bundle.providers || []);
  updateWorkflow(project);
}

function updateWorkflow(project) {
  const scenes = project.document.timeline?.scenes || [];
  const exports = project.document.exports || [];
  const steps = $$(".workflow-step");
  steps.forEach((step, index) => {
    step.classList.toggle("done", (index === 0 && !!project.document.brief) || (index === 1 && scenes.length) || (index === 2 && exports.length));
    step.classList.toggle("active", (index === 0 && !project.document.brief) || (index === 1 && project.document.brief && !scenes.length) || (index === 2 && scenes.length && !exports.length));
  });
}

function renderAssets(assets) {
  const list = $("#asset-list");
  list.replaceChildren();
  for (const asset of assets) {
    const row = document.createElement("div");
    row.className = "asset-row";
    const icon = document.createElement("span");
    icon.className = "asset-type";
    icon.textContent = asset.kind === "audio" ? "♫" : "▧";
    const info = document.createElement("div");
    info.className = "asset-info";
    const name = document.createElement("strong");
    name.textContent = asset.name;
    const meta = document.createElement("small");
    const duration = asset.duration_seconds ? ` · ${Math.round(asset.duration_seconds)}${t("seconds")}` : "";
    meta.textContent = `${formatBytes(asset.size_bytes)}${duration}`;
    info.append(name, meta);
    const badge = document.createElement("span");
    badge.className = "asset-badge";
    badge.textContent = asset.kind === "video" ? t("sourceMedia") : "Audio";
    row.append(icon, info, badge);
    if (asset.kind === "audio" && state.bundle.project.mode === "prompt") {
      const music = document.createElement("button");
      music.className = "text-link";
      music.textContent = state.bundle.project.document.music_asset_id === asset.id ? "♫ ✓" : "♫";
      music.title = "Use as background music";
      music.addEventListener("click", async () => {
        try {
          await api(`/api/projects/${state.projectId}/document`, {
            method: "PATCH", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ music_asset_id: asset.id })
          });
          toast(t("saved")); await openProject(state.projectId);
        } catch (error) { toast(error.message, true); }
      });
      row.append(music);
    }
    list.append(row);
  }
}

function renderScenes(scenes) {
  const list = $("#scene-list");
  list.replaceChildren();
  if (!scenes.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.innerHTML = `<span>✳</span><p>${t("emptyScenes")}</p>`;
    list.append(empty);
    return;
  }
  scenes.forEach((scene, index) => {
    const card = document.createElement("article");
    card.className = "scene-card";
    card.dataset.sceneId = scene.id;
    const top = document.createElement("div");
    top.className = "scene-top";
    const number = document.createElement("span");
    number.className = "scene-number";
    number.textContent = String(index + 1).padStart(2, "0");
    const title = document.createElement("input");
    title.className = "scene-title-input";
    title.value = scene.title || `${t("clip")} ${index + 1}`;
    title.setAttribute("aria-label", t("title"));
    const duration = document.createElement("span");
    duration.className = "scene-duration";
    duration.textContent = `${Math.round(scene.duration_seconds || 0)}${t("seconds")}`;
    top.append(number, title, duration);
    const fields = document.createElement("div");
    fields.className = "scene-fields";
    const narration = scene.narration || "";
    const direction = scene.visual_direction || "";
    const caption = scene.caption_text || "";
    fields.append(
      makeSceneField(t("narration"), "narration", narration),
      makeSceneField(t("visualDirection"), "visual_direction", direction),
      makeSceneField(t("caption"), "caption_text", caption)
    );
    const durationInput = document.createElement("input");
    durationInput.className = "text-input scene-duration-edit";
    durationInput.type = "number";
    durationInput.min = "1";
    durationInput.max = "600";
    durationInput.step = "1";
    durationInput.value = String(Math.round(scene.duration_seconds || 6));
    durationInput.setAttribute("aria-label", t("targetDuration"));
    durationInput.style.marginTop = "8px";
    durationInput.style.width = "100px";
    durationInput.style.padding = "6px";
    fields.append(makeSceneField(t("targetDuration"), "duration_seconds", "", durationInput));
    card.append(top, fields);
    const save = async () => {
      const changes = {
        title: title.value,
        narration: card.querySelector('[data-field="narration"]')?.value || "",
        visual_direction: card.querySelector('[data-field="visual_direction"]')?.value || "",
        caption_text: card.querySelector('[data-field="caption_text"]')?.value || "",
        duration_seconds: Number(durationInput.value || 6)
      };
      try {
        await api(`/api/projects/${state.projectId}/scenes/${encodeURIComponent(scene.id)}`, {
          method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(changes)
        });
        toast(t("saved"));
      } catch (error) { toast(error.message, true); }
    };
    card.addEventListener("focusout", (event) => {
      if (event.target.matches("input,textarea")) save();
    });
    list.append(card);
  });
}

function makeSceneField(labelText, field, value, existingInput = null) {
  const wrapper = document.createElement("div");
  wrapper.className = "scene-field";
  const label = document.createElement("label");
  label.textContent = labelText;
  const input = existingInput || document.createElement("textarea");
  if (!existingInput) {
    input.value = value;
    input.dataset.field = field;
    input.maxLength = field === "narration" ? 4000 : 2000;
  }
  wrapper.append(label, input);
  return wrapper;
}

function renderHighlights(highlights) {
  const list = $("#highlight-list");
  list.replaceChildren();
  $("#highlight-footer").hidden = !highlights.length;
  for (const item of highlights) {
    const label = document.createElement("label");
    label.className = "highlight-item";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = item.id;
    checkbox.addEventListener("change", updateSelectionCount);
    const copy = document.createElement("div");
    copy.className = "highlight-copy";
    const title = document.createElement("strong");
    title.textContent = item.title;
    const excerpt = document.createElement("p");
    excerpt.textContent = item.transcript_excerpt || item.reason || "";
    const meta = document.createElement("div");
    meta.className = "highlight-meta";
    meta.textContent = `${formatTime(item.start_seconds)} – ${formatTime(item.end_seconds)} · ${Math.round(item.end_seconds - item.start_seconds)}${t("seconds")}`;
    copy.append(title, excerpt, meta);
    label.append(checkbox, copy);
    list.append(label);
  }
  updateSelectionCount();
}

function updateSelectionCount() {
  const count = $$("#highlight-list input:checked").length;
  $("#selected-count").textContent = `${count} ${t("selection")}`;
}

function renderExports(exports, jobs, deliveries = []) {
  const list = $("#export-list");
  list.replaceChildren();
  const latestRenderId = exports.at(-1)?.render_id;
  const results = exports.filter((item) => item.render_id === latestRenderId);
  $("#exports-card").hidden = !results.length && !jobs.some((job) => job.kind === "render_project");
  if (!results.length) {
    const job = jobs.find((item) => item.kind === "render_project");
    const p = document.createElement("div");
    p.className = "empty-state";
    p.innerHTML = `<span>${job?.status === "running" ? "◌" : "↗"}</span><p>${job ? `${job.message} · ${Math.round(job.progress)}%` : t("noExports")}</p>`;
    list.append(p);
    return;
  }
  results.forEach((item) => {
    const renderId = item.render_id;
    const ratio = item.aspect_ratio.replace(":", "x");
    const base = `/api/projects/${state.projectId}/exports/${renderId}/${ratio}`;
    const card = document.createElement("article");
    card.className = "export-item";
    const video = document.createElement("video");
    video.controls = true;
    video.preload = "metadata";
    video.src = `${base}/video.mp4`;
    const title = document.createElement("strong");
    title.textContent = `${item.aspect_ratio} · ${Math.round(item.duration_seconds || 0)}${t("seconds")}`;
    const details = document.createElement("small");
    details.textContent = `${item.width} × ${item.height}`;
    const links = document.createElement("div");
    links.className = "export-links";
    [["video.mp4", t("downloadVideo")], ["captions.srt", "SRT"], ["captions.vtt", "VTT"], ["project.json", t("downloadProject")]].forEach(([file, label]) => {
      const a = document.createElement("a");
      a.href = `${base}/${file}`;
      a.download = file;
      a.textContent = label;
      links.append(a);
    });
    const deliveryList = document.createElement("div");
    deliveryList.className = "delivery-list";
    deliveries.filter((entry) => entry.render_id === renderId && entry.aspect_ratio === item.aspect_ratio)
      .forEach((entry) => {
        const row = document.createElement("small");
        const status = ["published", "uploaded"].includes(entry.status) ? t("published") : t("publishedProcessing");
        row.textContent = `${entry.platform.toUpperCase()} · ${status}${entry.url ? ` · ${entry.url}` : ""}`;
        deliveryList.append(row);
      });
    const publish = document.createElement("button");
    publish.type = "button";
    publish.className = "publish-export-button";
    publish.textContent = `${t("publishAction")} ↗`;
    publish.addEventListener("click", () => openPublishDialog(item));
    card.append(video, title, details, links, deliveryList, publish);
    list.append(card);
  });
}

function renderProvider(providers) {
  const current = providers.find((item) => item.selected);
  const host = $("#provider-current");
  host.replaceChildren();
  const dot = document.createElement("span");
  dot.className = "provider-dot";
  dot.style.background = current?.configured ? "#c8f36a" : "#c68b52";
  const text = document.createElement("span");
  text.textContent = current ? `${current.label} · ${current.configured ? t("providerConfigured") : t("notConfigured")}` : t("waiting");
  host.append(dot, text);
}

async function uploadFile(file) {
  if (!state.projectId || !file) return;
  const progress = $("#upload-progress");
  progress.hidden = false;
  try {
    const form = new FormData();
    form.append("file", file);
    await api(`/api/projects/${state.projectId}/upload`, { method: "POST", body: form });
    toast(t("fileUploaded"));
    await openProject(state.projectId);
  } catch (error) {
    toast(`${t("uploadError")} ${error.message}`, true);
  } finally {
    progress.hidden = true;
  }
}

async function enqueue(kind) {
  if (!state.projectId) return;
  let path, body;
  if (kind === "script") {
    path = `/api/projects/${state.projectId}/script`;
    body = { language: $("#project-language").value, target_duration_seconds: 60 };
  } else if (kind === "analyze") {
    path = `/api/projects/${state.projectId}/analyze`;
    body = { model: "small" };
  } else {
    const ratios = $$('input[name="format"]:checked').map((input) => input.value);
    if (!ratios.length) return toast("Choose an output format.", true);
    path = `/api/projects/${state.projectId}/render`;
    body = { aspect_ratios: ratios, include_captions: $("#captions-toggle").checked, use_tts: $("#tts-toggle").checked };
  }
  try {
    const result = await api(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const job = result.job;
    if (kind === "script") toast(t("checking"));
    if (kind === "render") toast(t("renderQueued"));
    await pollJob(job.id, kind);
  } catch (error) {
    const message = kind === "script" ? `${error.message}` : kind === "analyze" ? `${error.message}` : `${error.message}`;
    toast(message || t("genericError"), true);
  }
}

async function pollJob(jobId, kind) {
  if (state.polling) return;
  state.polling = true;
  try {
    while (true) {
      const job = await api(`/api/jobs/${jobId}`);
      if (state.projectId === job.project_id) {
        $("#project-status").textContent = t(job.status === "completed" ? "ready" : job.status === "failed" ? "failed" : "processing");
        if (kind === "render") renderExports([], [{ ...job, kind: "render_project" }]);
      }
      if (["completed", "failed", "cancelled"].includes(job.status)) {
        if (job.status === "failed") toast(`${t("jobFailed")}: ${job.error || job.message}`, true);
        else if (kind === "script") toast(t("scriptGenerated"));
        else if (kind === "analyze") toast(t("analysisDone"));
        if (state.projectId === job.project_id) await openProject(job.project_id);
        return;
      }
      await new Promise((resolve) => setTimeout(resolve, 1200));
    }
  } catch (error) {
    toast(error.message || t("genericError"), true);
  } finally {
    state.polling = false;
  }
}

function formatBytes(value) {
  if (!value) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const power = Math.min(Math.floor(Math.log(value) / Math.log(1024)), units.length - 1);
  return `${(value / 1024 ** power).toFixed(power ? 1 : 0)} ${units[power]}`;
}
function formatTime(value) {
  const seconds = Math.max(0, Math.floor(value || 0));
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

async function saveProjectSettings() {
  if (!state.projectId) return;
  const formats = $$('input[name="format"]:checked').map((item) => item.value);
  if (!formats.length) return;
  try {
    await api(`/api/projects/${state.projectId}`, {
      method: "PATCH", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language: $("#project-language").value, aspect_ratios: formats })
    });
  } catch (error) { toast(error.message, true); }
}

function openModal() { $("#integrations-modal").hidden = false; }
function closeModal() { $("#integrations-modal").hidden = true; $("#publish-modal").hidden = true; }

function platformPreflight() {
  return state.publishOptions.find((item) => item.platform === $("#publish-platform").value);
}

function updatePublishState() {
  const platform = $("#publish-platform").value;
  const item = platformPreflight();
  const privacyLabel = $("label[for='publish-privacy']");
  const privacySelect = $("#publish-privacy");
  const shareOption = $("#share-feed-option");
  const aiOption = $("#ai-label-option");
  const privacyOptions = platform === "tiktok" ? (item?.privacy_options || [])
    : platform === "youtube" ? ["private", "unlisted", "public"] : [];
  privacyLabel.hidden = platform === "instagram";
  privacySelect.hidden = platform === "instagram";
  shareOption.hidden = platform !== "instagram";
  aiOption.hidden = platform !== "tiktok";
  const previous = privacySelect.value;
  privacySelect.replaceChildren();
  for (const value of privacyOptions) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = t(value.toLowerCase()) === value.toLowerCase() ? value : t(value.toLowerCase());
    privacySelect.append(option);
  }
  if (privacyOptions.includes(previous)) privacySelect.value = previous;
  else if (privacyOptions.includes("private")) privacySelect.value = "private";
  else if (privacyOptions.includes("SELF_ONLY")) privacySelect.value = "SELF_ONLY";
  const box = $("#publish-preflight");
  box.replaceChildren();
  const ready = Boolean(item?.ready);
  const status = document.createElement("strong");
  status.textContent = ready ? t("preflightReady") : t("preflightBlocked");
  box.classList.toggle("ready", ready);
  box.classList.toggle("blocked", !ready);
  box.append(status);
  if (item?.requirements?.length) {
    const list = document.createElement("ul");
    item.requirements.forEach((requirement) => {
      const li = document.createElement("li");
      li.textContent = requirement;
      list.append(li);
    });
    box.append(list);
  }
  const title = $("#publish-post-title").value.trim();
  const description = $("#publish-description").value.trim();
  const combinedLength = [title, description].filter(Boolean).join("\n\n").length;
  const invalidTitle = platform === "youtube" && title.length > 100;
  const invalidCaption = ["instagram", "tiktok"].includes(platform) && combinedLength > 2200;
  if (invalidTitle || invalidCaption) {
    const warning = document.createElement("p");
    warning.textContent = platform === "youtube" ? "YouTube: max. 100 characters in the title." : `${platform}: max. 2,200 characters for title and caption.`;
    box.append(warning);
  }
  $("#confirm-publish").disabled = !ready || !$("#publish-confirm-checkbox").checked || !title || invalidTitle || invalidCaption;
}

async function openPublishDialog(exportItem) {
  state.publishing = exportItem;
  $("#publish-render-id").value = exportItem.render_id;
  $("#publish-aspect").value = exportItem.aspect_ratio;
  $("#publish-post-title").value = exportItem.title || state.bundle?.project?.document?.script?.title || state.bundle?.project?.title || "";
  $("#publish-description").value = exportItem.description || state.bundle?.project?.document?.brief || "";
  $("#publish-platform").value = "youtube";
  $("#publish-confirm-checkbox").checked = false;
  $("#publish-preflight").textContent = t("preflightLoading");
  $("#confirm-publish").disabled = true;
  $("#publish-modal").hidden = false;
  try {
    const ratio = encodeURIComponent(exportItem.aspect_ratio.replace(":", "x"));
    state.publishOptions = await api(`/api/projects/${encodeURIComponent(state.projectId)}/exports/${encodeURIComponent(exportItem.render_id)}/${ratio}/publishers`);
    updatePublishState();
  } catch (error) {
    $("#publish-preflight").textContent = error.message || t("genericError");
  }
  $("#publish-post-title").focus();
}

async function submitPublish() {
  const button = $("#confirm-publish");
  if (button.disabled || !state.publishing) return;
  button.disabled = true;
  const payload = {
    render_id: $("#publish-render-id").value,
    aspect_ratio: $("#publish-aspect").value,
    platform: $("#publish-platform").value,
    title: $("#publish-post-title").value.trim(),
    description: $("#publish-description").value.trim(),
    privacy_level: $("#publish-privacy").value || "private",
    confirm: true,
    share_to_feed: $("#share-to-feed").checked,
    ai_generated: $("#ai-generated-label").checked
  };
  try {
    await api(`/api/projects/${encodeURIComponent(state.projectId)}/publish`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
    });
    $("#publish-modal").hidden = true;
    toast(t("publishSuccess"));
    await openProject(state.projectId);
  } catch (error) {
    toast(error.message || t("genericError"), true);
  } finally {
    updatePublishState();
  }
}

$("#mode-prompt").addEventListener("click", () => setMode("prompt"));
$("#mode-repurpose").addEventListener("click", () => setMode("repurpose"));
$("#create-form").addEventListener("submit", createProject);
$("#new-project").addEventListener("click", () => { showWelcome(); $("#project-title").focus(); });
$("#generate-script").addEventListener("click", () => enqueue("script"));
$("#analyze-media").addEventListener("click", () => enqueue("analyze"));
$("#render-button").addEventListener("click", () => enqueue("render"));
$("#browse-file").addEventListener("click", () => $("#project-file").click());
$("#project-file").addEventListener("change", (event) => uploadFile(event.target.files?.[0]));
$("#source-file").addEventListener("change", (event) => {
  state.pendingSourceFile = event.target.files?.[0] || null;
  if (state.pendingSourceFile) toast(state.language === "es" ? "Crea el proyecto para importar el archivo." : "Create the project to import this file.");
});
$("#dropzone").addEventListener("click", (event) => { if (!event.target.closest("button")) $("#project-file").click(); });
$("#dropzone").addEventListener("dragover", (event) => { event.preventDefault(); $("#dropzone").classList.add("dragging"); });
$("#dropzone").addEventListener("dragleave", () => $("#dropzone").classList.remove("dragging"));
$("#dropzone").addEventListener("drop", (event) => { event.preventDefault(); $("#dropzone").classList.remove("dragging"); uploadFile(event.dataTransfer.files?.[0]); });
$("#use-highlights").addEventListener("click", async () => {
  const ids = $$("#highlight-list input:checked").map((input) => input.value);
  if (!ids.length) return toast(t("chooseClips"), true);
  try {
    await api(`/api/projects/${state.projectId}/highlights`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ selected_ids: ids })
    });
    toast(t("clipsSelected")); await openProject(state.projectId);
  } catch (error) { toast(error.message, true); }
});
$("#project-language").addEventListener("change", saveProjectSettings);
$$('input[name="format"]').forEach((item) => item.addEventListener("change", saveProjectSettings));
$("#refresh-providers").addEventListener("click", async () => {
  try { const data = await api("/api/providers"); renderProvider(data.text); }
  catch (error) { toast(error.message, true); }
});
$("#open-integrations").addEventListener("click", openModal);
$("#open-integrations-top").addEventListener("click", openModal);
$("#close-integrations").addEventListener("click", closeModal);
$("#integrations-modal").addEventListener("click", (event) => { if (event.target.id === "integrations-modal") closeModal(); });
$("#close-publish").addEventListener("click", closeModal);
$("#publish-modal").addEventListener("click", (event) => { if (event.target.id === "publish-modal") closeModal(); });
$("#publish-platform").addEventListener("change", updatePublishState);
$("#publish-confirm-checkbox").addEventListener("change", updatePublishState);
$("#publish-post-title").addEventListener("input", updatePublishState);
$("#publish-description").addEventListener("input", updatePublishState);
$("#confirm-publish").addEventListener("click", submitPublish);
$("#language-toggle").addEventListener("click", () => {
  state.language = state.language === "es" ? "en" : "es";
  localStorage.setItem("avs-language", state.language);
  applyLanguage();
});
document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); showWelcome(); $("#project-title").focus(); }
  if (event.key === "Escape") closeModal();
});

applyLanguage();
loadProjects();
api("/api/providers").then((data) => renderProvider(data.text)).catch(() => {});
\n