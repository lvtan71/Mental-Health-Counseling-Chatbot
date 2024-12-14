# About Dataset

This dataset is designed to support mental health counseling. It comprises a collection of questions regarding mental health symptoms, along with corresponding diagnoses and advice based on the provided information. The goal of collecting this data is to develop a chatbot capable of providing suggestions and preliminary diagnoses to users based on their described symptoms.

## About Data Collection Methodology

The data collection process involves aggregating information from academic documents, mental health research, and simulated data by AI models such as the GPT-4o-mini. Each data entry in the collection includes a user statement accompanied by reference information from specialized documents, thereby providing suitable diagnoses and advice.

### Description of the Data

The data is organized in JSON format, with each entry containing fields such as `query` (question/information from the user), `reference_contexts` (context references from documents), and `reference_answer` (diagnosis and advice). This data is stored on GitHub in the directory structure as shown below:

```
Root Dir/
  - evaluate/
    - data/
      - data.json
      - README.md
```

### Sample of the Dataset

Below is a sample entry from the dataset to provide a better understanding of its structure and content:

```json
{
    "query": "Lời khai: Tôi thường gặp khó khăn trong việc giao tiếp với người khác, đặc biệt là khi phải chia sẻ thông tin hoặc tham gia vào các cuộc trò chuyện xã hội. Tôi cảm thấy mình không thể điều chỉnh cách nói của mình cho phù hợp với từng tình huống, và điều này khiến tôi cảm thấy lạc lõng.",
    "query_by": {
        "model_name": "gpt-4o-mini",
        "type": "ai"
    },
    "reference_contexts": [
        "# 1.2.5 Rối loạn giao tiếp xã hội\n\nA. Khó khăn dai dẳng trong giao tiếp xã hội dùng lời và không dùng lời biểu thị bởi tất cả những điều sau:\n\n1. Suy giảm trong sử dụng giao tiếp cho các mục đích xã hội, như chào hỏi và chia sẻ thông tin bằng cách thức phù hợp với hoàn cảnh xã hội.\n2. Suy giảm khả năng thay đổi giao tiếp cho phù hợp hoàn cảnh hoặc nhu cầu của người nghe, như nói trong lớp học khác trong sân chơi, nói chuyện với 1 đứa trẻ hơn với khác biệt 1 người lớn, và tránh sử dụng ngôn ngữ quá hình thức.\n3. Khó tuân theo những nguyên tắc giao tiếp và người nói chuyện, như quay trở lại mạch giao tiếp, nói lại bằng các từ khác khi bị hiểu sai, và biết cách sử dụng lời nói và ký hiệu không lời để điều chỉnh tương tác.\n4. Khó khăn trong việc hiểu những điều không nói thẳng (phải suy luận) và không theo nghĩa đen hoặc nước đôi (thành ngữ, câu đùa, phép ẩn dụ, đa nghĩa mà hiểu phụ thuộc vào tình huống).\n\nB. Sự suy giảm dẫn đến hạn chế hiệu quả giao tiếp, tham gia xã hội, quan hệ xã hội, thành tích học tập hoặc hoạt động nghề nghiệp, riêng lẻ hoặc kết hợp.\n\nC. Khởi phát của những triệu chứng trong thời kỳ phát triển sớm (cũng có thể không đầy đủ rõ ràng đến khi đòi hỏi của giao tiếp xã hội vượt quá khả năng hạn chế của trẻ).\n\nD. Các triệu chứng không do một bệnh cơ thể hoặc bệnh thần kinh hoặc khả năng cấu trúc từ và ngữ pháp hạn chế, và không được giải thích tốt hơn bởi rối loạn phổ tự kỷ, rối loạn phát triển trí tuệ, chậm phát triển tổng thể, hoặc một rối loạn tâm thần khác.\n"
    ],
    "reference_answer": "Chẩn đoán:\n\nDựa trên lời khai của bạn, có thể thấy rằng bạn đang gặp phải những khó khăn trong giao tiếp xã hội, đặc biệt là trong việc chia sẻ thông tin và điều chỉnh cách nói cho phù hợp với từng tình huống. Những triệu chứng này có thể liên quan đến Rối loạn giao tiếp xã hội, mà theo thông tin ngữ cảnh, bao gồm các khó khăn trong việc sử dụng giao tiếp cho các mục đích xã hội, điều chỉnh giao tiếp theo hoàn cảnh, và tuân theo các nguyên tắc giao tiếp.",
    "reference_answer_by": {
        "model_name": "gpt-4o-mini",
        "type": "ai"
    }
}
```

## Online Repository Link

* [Mental Health Counseling Dataset](https://github.com/lvtan71/Mental-Health-Counseling-Chatbot/tree/main/evaluate/data) - Link to the data repository.

## Authors

* **21120554 - Lê Văn Tấn**
* **21120527 - Nguyễn Thế Phong**
* **18120445 - Hoàng Nguyễn Hải Long**
