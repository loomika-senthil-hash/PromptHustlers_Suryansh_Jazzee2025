from streamlit.components.v1 import html
import gv_config

def show_voice_widget():
    html(f'''
    <button id="vapi-btn">🎙️ Speak</button>
    <script src="https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js"></script>
    <script>
      let vapiInstance = null;

      (function(d,t){{
        const s = d.createElement(t), h = d.getElementsByTagName(t)[0];
        s.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
        s.async = s.defer = true;
        h.parentNode.insertBefore(s, h);
        s.onload = () => {{
          console.log("✅ SDK loaded. Initializing...");
          vapiInstance = window.vapiSDK.run({{
            apiKey: "{gv_config.VAPI_PUBLIC_KEY}",
            assistant: "{gv_config.VAPI_ASSISTANT_ID}"
          }});
          console.log("🔧 vapiInstance:", vapiInstance);

          // 👉 Proper event listeners:
          vapiInstance.on("call-start", () => console.log("➡️ Call started"));
          vapiInstance.on("message", msg => {{
            console.log("📨 Message:", msg);
            if (msg.type === "audio") {{
              new Audio(URL.createObjectURL(new Blob([msg.audio], {{ type: "audio/wav" }}))).play();
            }} else if (msg.text) {{
              console.log("💬 Text:", msg.text);
            }}
          }});
          vapiInstance.on("call-end", () => console.log("⏹️ Call ended"));
          vapiInstance.on("error", err => console.error("⚠️ SDK error caught:", err));
        }};
      }})(document,"script");

      document.getElementById("vapi-btn").onclick = () => {{
        console.log("🎙️ Speak clicked");
        vapiInstance.start({{ assistant: "{gv_config.VAPI_ASSISTANT_ID}" }})
          .then(res => console.log("✅ start() succeeded:", res))
          .catch(err => console.error("❌ start() failed:", err));
      }};
    </script>
    ''', height=250)

