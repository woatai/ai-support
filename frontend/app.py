import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"


st.set_page_config(page_title="AI Support")

st.title("AI Support")

message = st.text_area("请输入客户问题", placeholder="例如：我的订单什么时候发货？")

if st.button("发送", type="primary"):
    if not message.strip():
        st.warning("请先输入客户问题。")
    else:
        with st.spinner("AI 客服正在回复..."):
            try:
                response = requests.post(API_URL, json={"message": message.strip()}, timeout=60)
                data = response.json()
                response.raise_for_status()
                reply = data.get("reply", "")
            except requests.exceptions.RequestException as exc:
                detail = ""
                if getattr(exc, "response", None) is not None:
                    try:
                        detail = exc.response.json().get("detail", "")
                    except ValueError:
                        detail = exc.response.text
                st.error(f"请求后端失败：{detail or exc}")
            else:
                st.subheader("AI 客服回复")
                st.write(reply)
