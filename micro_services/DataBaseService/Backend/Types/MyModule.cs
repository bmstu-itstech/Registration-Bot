namespace DataBaseService.Backend.Types
{
    public class MyModule
    {

        public MyModule()
        {

        }
       
        public string Question { get; set; }
        public string Type { get; set; }
        public string Title { get; set; }
        public List<int> Next_ids { get; set; }
        public List<int> Answers { get; set; }

    }
}
