import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="유튜브 & 틱톡 통합 모바일 다운로더", page_icon="📲", layout="centered")

st.title("📲 모바일 영상/음원 다운로더")
st.markdown("유튜브 또는 틱톡 링크를 넣고 아래 버튼을 누르면 스마트폰으로 바로 저장됩니다.")
st.markdown("*(이 어플은 깃허브(GitHub)와 Streamlit Cloud를 통해 무료로 호스팅됩니다)*")

url = st.text_input("🔗 동영상 링크 입력 (유튜브/틱톡)")
format_choice = st.radio("포맷 선택", ["영상 (MP4)", "음원 (MP3 / 오디오)"], horizontal=True)

if st.button("다운로드 처리 시작", use_container_width=True):
    if not url:
        st.warning("먼저 다운로드할 링크를 입력해주세요!")
    else:
        with st.spinner("서버에서 다운로드 중입니다... 잠시만 기다려주세요⏳"):
            try:
                # 안전한 서버용 임시 폴더 생성
                temp_dir = tempfile.mkdtemp()
                
                ydl_opts = {
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                }
                
                if format_choice == "영상 (MP4)":
                    ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                else:
                    ydl_opts['format'] = 'bestaudio/best'
                    # 서버(Streamlit)에는 보통 ffmpeg가 내장되어 있어 mp3 변환이 수월합니다.
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    downloaded_file = ydl.prepare_filename(info)
                    
                    if format_choice == "음원 (MP3 / 오디오)":
                        downloaded_file = downloaded_file.rsplit('.', 1)[0] + '.mp3'

                # 다운로드 버튼 노출
                with open(downloaded_file, "rb") as file:
                    st.success("✅ 처리가 완료되었습니다! 아래 버튼을 눌러 기기(스마트폰)에 저장하세요.")
                    st.download_button(
                        label="📥 내 폰으로 파일 저장하기 (클릭)",
                        data=file,
                        file_name=os.path.basename(downloaded_file),
                        mime="video/mp4" if "영상" in format_choice else "audio/mpeg",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ 다운로드 오류가 발생했습니다: {str(e)}\n\n(영상이 비공개이거나 링크 형식이 잘못되었을 수 있습니다.)")
