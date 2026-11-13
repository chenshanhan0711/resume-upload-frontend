/* ============================================================
   01-frontend-resume-upload 交互脚本（纯原生 JS，无依赖、无服务器）
   职责：文件选择/拖拽 → 显示文件名；Finish 校验 → 可访问状态提示。
   ============================================================ */
(function () {
  "use strict";

  var fileInput = document.getElementById("file-input");
  var uploadArea = document.getElementById("upload-area");
  var fileStatus = document.getElementById("file-status");
  var fileName = document.getElementById("file-name");
  var btnBack = document.getElementById("btn-back");
  var btnFinish = document.getElementById("btn-finish");

  // 当前选中的文件
  var selectedFile = null;
  var MAX_FILE_SIZE = 5 * 1024 * 1024;
  var ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"];

  function setStatus(message, kind) {
    fileStatus.className = "file-status" + (kind ? " " + kind : "");
    // 保留状态图标前缀，正文用文本节点替换，避免 XSS（文件名可能含特殊字符）
    fileName.textContent = message;
  }

  function showFileName(file) {
    if (!file) {
      selectedFile = null;
      setStatus("No file selected", "");
      return;
    }

    var lowerName = String(file.name || "").toLowerCase();
    var allowedType = ALLOWED_EXTENSIONS.some(function (extension) {
      return lowerName.endsWith(extension);
    });
    if (!allowedType) {
      selectedFile = null;
      fileInput.value = "";
      setStatus("Please choose a PDF, DOC or DOCX file.", "error");
      return;
    }
    if (typeof file.size === "number" && file.size > MAX_FILE_SIZE) {
      selectedFile = null;
      fileInput.value = "";
      setStatus("File is larger than the 5 MB limit.", "error");
      return;
    }

    selectedFile = file;
    var size = "";
    if (typeof file.size === "number") {
      size = " · " + (file.size / 1024).toFixed(1) + " KB";
    }
    setStatus("Selected: " + file.name + size, "has-file");
  }

  function handleFiles(fileList) {
    if (!fileList || fileList.length === 0) {
      return;
    }
    showFileName(fileList[0]);
  }

  // 1) 点击 label 打开文件框：由 <label for="file-input"> 原生触发。
  // 2) 键盘：隐藏 input 是 sr-only（可聚焦），Tab 到它 + Enter/Space 原生打开。
  // 3) 选择文件后显示文件名。
  fileInput.addEventListener("change", function () {
    handleFiles(fileInput.files);
  });

  // 拖拽支持
  ["dragenter", "dragover"].forEach(function (evt) {
    uploadArea.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      uploadArea.classList.add("is-dragging");
    });
  });

  ["dragleave", "drop"].forEach(function (evt) {
    uploadArea.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      uploadArea.classList.remove("is-dragging");
    });
  });

  uploadArea.addEventListener("drop", function (e) {
    if (e.dataTransfer && e.dataTransfer.files) {
      handleFiles(e.dataTransfer.files);
    }
  });

  // 阻止浏览器默认打开被误拖到页面其它区域的文件的动作
  ["dragover", "drop"].forEach(function (evt) {
    window.addEventListener(evt, function (e) {
      e.preventDefault();
    });
  });

  // Finish：未选文件 → 可访问状态提示；已选 → 完成提示
  btnFinish.addEventListener("click", function () {
    if (!selectedFile) {
      setStatus("Please choose a file before finishing.", "error");
      return;
    }
    setStatus("Uploaded " + selectedFile.name + " — done!", "has-file");
  });

  // Last step：返回上一步（本演示仅含上传步骤，点击回到初始态）
  btnBack.addEventListener("click", function () {
    selectedFile = null;
    if (fileInput) {
      fileInput.value = "";
    }
    setStatus("Back to previous step (demo) — selection cleared.", "");
  });
})();
