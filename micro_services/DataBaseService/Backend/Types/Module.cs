namespace DataBaseService.Backend.Types
{
    public class Module
    {

        public Module()
        {

        }
       
        public string Question { get; set; }
        public string Type { get; set; }
        public string Title { get; set; }
        public List<int> Next_ids { get; set; }
        public List<int> Answers { get; set; }

    }
}
