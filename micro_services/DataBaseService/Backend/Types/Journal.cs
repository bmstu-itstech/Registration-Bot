namespace DataBaseService.Backend.Types
{
    public class Journal
    {
        public int Id { get; set; }
        public Dictionary<int, Module> Modules { get; set; }
    }
}
