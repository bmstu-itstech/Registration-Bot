namespace DataBaseService.Backend.Types
{
    public class Module
    {
        public Module(List<int> answers, List<int> next_ids, string question)
        {
            Answers = answers;
            Next_ids = next_ids;
            Question = question;
        }

        public string Question { get; set; }
        public List<int> Next_ids { get; set; }
        public List<int> Answers { get; set; }

    }
}
