using DataBaseService.Protos;

namespace DataBaseService.Backend.Types
{
    public class MyButton
    {
        public int Id { get; set; }

        public string Answer_text { get; set; }
        public int QuestionId { get; set; }
        public int NextQuestionId { get; set; }

        public static MyButton ConvertFromRPC(Button _button)
        {
            return new MyButton
            {
                Answer_text = _button.AnswerText,
                QuestionId = _button.QuestionId,
                NextQuestionId = _button.NextQuestionId
            };
        }
        public static Button ConvertToRPC(MyButton button)
        {
            return new Button
            {
                AnswerText = button.Answer_text,
                QuestionId = button.QuestionId,
                NextQuestionId = button.NextQuestionId
            };
        }

    }
}
