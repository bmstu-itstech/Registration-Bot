namespace DataBaseService.Backend.Types
{
    public class MyJournal
    {
        public int Id { get; set; }
        public Dictionary<int, MyModule> Modules { get; set; }
    }
}
