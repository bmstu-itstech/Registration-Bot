using Grpc.Core;
using DataBaseService.DataBase;
using DataBaseService.Protos;
using DataBaseService.Backend.Types;
using Journal = DataBaseService.Backend.Types.Journal;
using System.Linq;

namespace DataBaseService.Services.Bot
{
    public class BotWorkerService : BotWorker.BotWorkerBase
    {

        private readonly ILogger<BotWorkerService> _logger;

        public BotWorkerService(ILogger<BotWorkerService> logger)
        {
            _logger = logger;
        }
        public override Task<BaseResponse> CreateBot(CreateBotRequest request, ServerCallContext context)
        {
            _logger.LogInformation("Create new Bot Survey Request");

            string state = "OK";
            int code = 200;

            var journal = request.Journal;

            Journal my_journal = new Journal()
            {
                Modules = request.Journal.Modules.ToDictionary(m => m.Key, m => new Backend.Types.Module
                {
                    Answers = m.Value.Answers.ToList(),
                    Question = m.Value.Question,
                    Title = m.Value.Title,
                    Type = m.Value.Type,
                    Next_ids = m.Value.NextIds.ToList(),    
                })
            };

            //main code 
            try
            {


                var response = DataBase.BotSurvey.CreateNewBotSurvey(request.FromUser, my_journal);

                response.Wait();

                if (response.IsFaulted)
                {
                    state = "Erorr while Creating new Bot Survey";
                    code = 401;
                }

            }
            catch (Exception ex)
            {
                state = $"Erorr while Creating new Bot Survey\n{ex.Message}";
                code = 401;
            }


            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }

        public override Task<BaseResponse> DeleteBot(DeleteBotRequest request, ServerCallContext context)
        {

            _logger.LogInformation("Delete new Bot Request");

            string state = "OK";
            int code = 200;

            //main code 
            try
            {


                var response = DataBase.BotSurvey.DeleteBotSurvey(request.FromUser, request.BotId);

                response.Wait();

                if (response.IsFaulted)
                {
                    state = "Erorr while Deleting Bot Survey";
                    code = 401;
                }

            }
            catch (Exception ex)
            {
                state = $"Erorr while Deleting Bot Survey\n{ex.Message}";
                code = 401;
            }

            return Task.FromResult(new BaseResponse()
            {
                State = state,
                Code = code
            });
        }
    }
}
