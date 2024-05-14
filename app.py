import streamlit as st
from docx import Document
from transformers import pipeline

# Initialize the language correction model
corrector = pipeline("text2text-generation", model="bmd1905/vietnamese-correction")

def read_docx(file_path):
    doc = Document(file_path)
    return [paragraph.text for paragraph in doc.paragraphs]

def process_document(doc_content):
    MAX_LENGTH = 512
    result = ""
    for text in doc_content:
        corrected_text = corrector(text, max_length=MAX_LENGTH)[0]['generated_text']
        if text != corrected_text and text.strip() + ' .' != corrected_text:
            # Display the result
            st.subheader("Đề xuất:")
            result_with_color = ""
            for original_word, corrected_word in zip(text.split(), corrected_text.split()):
                # Tô màu các từ sai
                if original_word != corrected_word:
                    result_with_color += f"<span style='color:red'>{original_word}</span> "
                else:
                    result_with_color += f"{original_word} "

            st.markdown(result_with_color, unsafe_allow_html=True)

            st.write("- ")
            st.write(corrected_text)

            # differences = [(original_word, corrected_word) for original_word, corrected_word in zip(text.split(), corrected_text.split()) if original_word != corrected_word]
            # if differences:
            #     st.write("Thay đổi:")
            #     for original_word, corrected_word in differences:
            #         st.write(f"    > '{original_word}' (gốc) -> '{corrected_word}' (sửa)")
            # else:
            #     st.write("Không có gì cần sửa.")


    return result

# Streamlit app
def main():
    st.title("Gợi ý sửa lỗi chính tả")

    # File upload
    uploaded_file = st.file_uploader("Tải tệp tin định dạng docx", type="docx")

    if uploaded_file is not None:
        # Read and process the uploaded file
        doc_content = read_docx(uploaded_file)
        result = process_document(doc_content)

        # Display the result
        # st.subheader("Result:")
        # st.text_area("Corrected Text", value=result, height=400)


if __name__ == "__main__":
    main()
