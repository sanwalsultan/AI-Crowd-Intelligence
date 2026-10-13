import streamlit as st
from pathlib import Path
import subprocess
import time


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Crowd Intelligence",
    page_icon="🚨",
    layout="wide"
)


# =====================================
# STYLE
# =====================================

st.markdown(
"""
<style>

.main-title {
    font-size:42px;
    font-weight:700;
    text-align:center;
    color:#00ff99;
}

.card {

    background:#161b22;
    padding:20px;
    border-radius:15px;
    margin:15px 0px;

}

</style>
""",
unsafe_allow_html=True
)



# =====================================
# PATHS
# =====================================

PROJECT_DIR = Path.cwd()


INPUT_FOLDER = (
    PROJECT_DIR
    /
    "input"
    /
    "crowd"
)


OUTPUT_VIDEO = (
    PROJECT_DIR
    /
    "output"
    /
    "crowd_intelligence_final.mp4"
)


STREAMLIT_VIDEO = (
    PROJECT_DIR
    /
    "output"
    /
    "crowd_streamlit.mp4"
)


REPORT_FOLDER = (
    PROJECT_DIR
    /
    "output"
    /
    "reports"
)



# =====================================
# FUNCTIONS
# =====================================


def run_ai_pipeline():

    result = subprocess.run(

        [
            "python",
            "src/main.py"
        ],

        capture_output=True,

        text=True

    )


    if result.returncode != 0:

        st.error(result.stderr)

        return False


    return True




def convert_video():

    command = [

        "ffmpeg",

        "-y",

        "-i",

        str(OUTPUT_VIDEO),

        "-vcodec",

        "libx264",

        "-pix_fmt",

        "yuv420p",

        "-preset",

        "fast",

        str(STREAMLIT_VIDEO)

    ]


    result = subprocess.run(

        command,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE

    )


    if STREAMLIT_VIDEO.exists():

        return True


    st.error(
        result.stderr.decode()
    )


    return False





# =====================================
# HEADER
# =====================================


st.markdown(

"""
<div class="main-title">

🚨 AI Crowd Intelligence System

</div>

""",

unsafe_allow_html=True

)



st.markdown(

"""
<div class="card">

<b>Computer Vision Surveillance Platform</b>

<br><br>

✅ Crowd Detection  
<br>
✅ Person Tracking  
<br>
✅ Face Mask Detection  
<br>
✅ Weapon Detection  
<br>
✅ Crowd Density Analysis  
<br>
✅ Heatmap Generation  
<br>
✅ Crowd Flow Analysis  
<br>
✅ Automated Reporting  

</div>

""",

unsafe_allow_html=True

)



# =====================================
# SIDEBAR
# =====================================


st.sidebar.title(
    "🎛 Control Panel"
)


uploaded_file = st.sidebar.file_uploader(

    "Upload CCTV Video",

    type=[
        "mp4",
        "avi",
        "mov"
    ]

)



start = st.sidebar.button(
    "🚀 Start Analysis"
)



# =====================================
# PROCESS
# =====================================


if start:


    if uploaded_file is None:


        st.warning(
            "Please upload video first"
        )


    else:


        INPUT_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )


        input_video = (
            INPUT_FOLDER
            /
            uploaded_file.name
        )


        with open(
            input_video,
            "wb"
        ) as f:


            f.write(
                uploaded_file.read()
            )



        st.success(
            "Video uploaded"
        )


        progress = st.progress(0)


        status = st.empty()



        for i in range(100):


            progress.progress(
                i+1
            )


            status.write(
                f"Preparing AI Pipeline {i+1}%"
            )


            time.sleep(0.01)



        st.info(
            "Running AI analysis..."
        )



        success = run_ai_pipeline()



        if success:


            st.success(
                "AI Processing Completed"
            )


            if OUTPUT_VIDEO.exists():


                st.info(
                    "Converting video for browser playback..."
                )


                convert_video()



# =====================================
# SHOW RESULT
# =====================================


st.divider()


st.header(
    "📹 Analysis Result"
)



if STREAMLIT_VIDEO.exists():


    size = (
        STREAMLIT_VIDEO.stat().st_size
        /
        (1024*1024)
    )


    st.success(

        f"Video Ready | {size:.2f} MB"

    )



    video_bytes = (

        STREAMLIT_VIDEO

        .read_bytes()

    )


    st.video(

        video_bytes,

        format="video/mp4"

    )


elif OUTPUT_VIDEO.exists():


    st.warning(
        "Video conversion pending"
    )


else:


    st.info(
        "Run analysis to generate result"
    )



# =====================================
# REPORT
# =====================================


st.divider()


st.header(
    "📊 Reports"
)



if REPORT_FOLDER.exists():


    reports = list(

        REPORT_FOLDER.glob(
            "*.csv"
        )

    )


    if reports:


        latest = sorted(
            reports
        )[-1]



        with open(
            latest,
            "rb"
        ) as file:


            st.download_button(

                label="⬇ Download Report",

                data=file,

                file_name=latest.name,

                mime="text/csv"

            )

    else:

        st.info(
            "No reports available"
        )


else:

    st.info(
        "Report folder not created"
    )