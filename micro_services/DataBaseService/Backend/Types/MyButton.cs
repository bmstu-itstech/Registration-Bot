using DataBaseService.Protos;

namespace DataBaseService.Backend.Types
{
    public class MyButton
    {
        public int Id { get; set; }
        public string Answer { get; set; }
        public int NextId { get; set; }
        public int Question_id { get; set; }

        public static MyButton ConvertFromRPC(Button _button)
        {
            return new MyButton
            {
                Answer = _button.Answer,
                NextId = _button.NextId
            };
        }
        public static Button ConvertToRPC(MyButton button)
        {
            return new Button
            {
                Answer = button.Answer,
                NextId = button.NextId
            };
        }

    }
}
