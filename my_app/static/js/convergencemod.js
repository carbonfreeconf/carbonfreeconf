function getSyncScriptParamsmod() {
         var scripts = document.getElementsByTagName('script');
         var lastScript = scripts[scripts.length-1];
         var scriptName = lastScript;
         return {
             idconv : scriptName.getAttribute('idconv'),
             usern : scriptName.getAttribute('usern'),
         };
 }

const getidmod=getSyncScriptParamsmod();

const defaultData2mod = 'Write here what you want to say in real time to other organizers/moderators...';

if (getidmod.usern != ''){
  var usernamemod=getidmod.usern//usern.outerHTML;
  //console.log(username+'ghfdd'+Object.prototype.toString.call(username));
  //document.getElementById("username").textContent = username;
}
else{
  var usernamemod = "User-" + Math.round(Math.random() * 10000);
}

var myEle3 = document.getElementById("usernamemod");
  if(myEle3){
    document.getElementById("usernamemod").innerHTML = usernamemod;
  }


///////////////////////////////////////////////////////////////////////////////
// Connect and Open the Model
///////////////////////////////////////////////////////////////////////////////

// Connect anonymously using the generated display name
Convergence.connectAnonymously(CONVERGENCE_URL, usernamemod).then(domain => {
  return domain.models().openAutoCreate({
    collection: "convergence-joinconfmod",
    id: getidmod.idconv,
    ephemeral: false,
    data: {
      text: defaultData2mod
    }
  });
}).then(model => {
  const rtsmod = model.elementAt(["text"]);
  //console.log(rts.type());
  bindTextareamod(rtsmod);
  initSharedSelectionmod(rtsmod);
}).catch(error => {
  console.error(error);
});

///////////////////////////////////////////////////////////////////////////////
// Text Editor
///////////////////////////////////////////////////////////////////////////////
const textareamod = document.getElementById("textareamod");
let textEditormod;

// Bind the text area to the real time string
function bindTextareamod(rts) {
  // Set the initial data, and set the cursor to the beginning.
  textareamod.value = rts.value();
  //alert(rts.value());
  //alert(gettest);
  textareamod.selectionStart = 0;
  textareamod.selectionEnd = 0;

  // Create the editor utility passing callbacks to bind local events to
  // the RealtimeString.
  textEditormod = new HtmlTextCollabExt.CollaborativeTextArea({
    control: textareamod,
    onInsert: (index, value) => rts.insert(index, value),
    onDelete: (index, length) => rts.remove(index, length),
    onSelectionChanged: sendLocalSelectionmod
  });

  // Listen to remote events and pass them to the editor utility
  rts.on(Convergence.StringInsertEvent.NAME, (e) => textEditormod.insertText(e.index, e.value));
  rts.on(Convergence.StringRemoveEvent.NAME, (e) => textEditormod.deleteText(e.index, e.value.length));
}

///////////////////////////////////////////////////////////////////////////////
// Share Selection Functions
///////////////////////////////////////////////////////////////////////////////
const colorAssignermod = new ConvergenceColorAssigner.ColorAssigner();

let localSelectionReferencemod;

function initSharedSelectionmod(rts) {
  // Create a local reference that will be used to send the local
  // users selection and cursor.
  localSelectionReferencemod = rts.rangeReference("selection");

  // Set and share the local selection.
  sendLocalSelectionmod();
  localSelectionReferencemod.share();

  // Get all existing "selection" references from the RealTimeString
  // and create remote selection cue for each.
  const referencesmod = rts.references({key: "selection"});
  referencesmod.forEach((reference) => {
    if (!reference.isLocal()) {
      addRemoteSelectionmod(reference);
    }
  });

  // Listen to the "reference" event which will be fired
  // when a new remote user shares their selection.
  rts.on("reference", (e) => {
      //alert('ok'+gettest);
    if (e.reference.key() === "selection") {
      addRemoteSelectionmod(e.reference);
    }
  });
}

function sendLocalSelectionmod() {
  const selectionmod = textEditormod.selectionManager().getSelection();
  localSelectionReferencemod.set({start: selectionmod.anchor, end: selectionmod.target});
  //alert('ok2 '+gettest.test);
}

function addRemoteSelectionmod(reference) {
  const colormod = colorAssignermod.getColorAsHex(reference.sessionId());
  const remoteRangemod = reference.value();

  // Gets the text editors SelectionManager.
  const selectionManagermod = textEditormod.selectionManager();

  // Add a new collaborator to the text editor.
  //console.log('ui'+reference.user().displayName);
  selectionManagermod.addCollaborator(
      reference.sessionId(),
      reference.user().displayName,
      colormod,
      {anchor: remoteRangemod.start, target: remoteRangemod.end});

  // Monitor the events from the remote reference and update the
  // remote users selection in the SelectionManager.
  reference.on("cleared", () => selectionManagermod.removeCollaborator(reference.sessionId()) );
  reference.on("disposed", () => selectionManagermod.removeCollaborator(reference.sessionId()) );
  reference.on("set", (e) => {
    const selectionmod = reference.value();
    const collaboratormod = selectionManagermod.getCollaborator(reference.sessionId());
    collaboratormod.setSelection({anchor: selectionmod.start, target: selectionmod.end});
    if (!e.synthetic) {
      collaboratormod.flashCursorToolTip(2);
    }
  });
}
