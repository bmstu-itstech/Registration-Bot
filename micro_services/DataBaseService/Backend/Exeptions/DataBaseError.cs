using System.Runtime.Serialization;

namespace DataBaseService.Backend.Exeptions
{
    public class DataBaseError : Exception
    {
        public DataBaseError(string? message) : base(message)
        {
        }

        public override string Message => base.Message;
    }
}
