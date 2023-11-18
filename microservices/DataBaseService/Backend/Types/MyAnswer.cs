using DataBaseService.Protos;

namespace DataBaseService.Backend.Types
{

    public class MyAnswer
    {
        public int Module_Id { get; set; }
        public string Answer { get; set; }
    
        private static int GetAnswerInt(string answer)
        {
            return int.Parse(answer);
        }
        private static long GetAnswerLong(string answer)
        {
            return long.Parse(answer);
        }
        private static bool GetAnswerBool(string answer) 
        {
            return bool.Parse(answer);
        }
        private static DateTime GetAnswerDate(string answer) 
        {
            return DateTime.Parse(answer); 
        }

        public static MyAnswer ConvertFromRPC(Answer _answer)
        {
            return new MyAnswer()
            {
                Answer = _answer.Answer_,
                Module_Id = _answer.ModuleId,

            };
        }

    }

   
}
