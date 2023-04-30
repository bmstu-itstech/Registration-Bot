using DataBaseService.Protos;

namespace DataBaseService.Backend.Types
{
    public class MyJournal
    {

        public Dictionary<int, MyModule> Modules { get; set; }

        public static MyJournal ConvertFromRPC(Journal _journal)
        {
            return new MyJournal()
            {
                Modules = _journal.Modules.ToDictionary(m => m.Key, m => MyModule.ConvertFromRPC(m.Value))
            };
        }


    }
}

