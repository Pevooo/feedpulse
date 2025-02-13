namespace Api.Service.Abstracts
{
    public interface IEmailService
    {
        public Task<string> SendEmail(string email, string Message, string? reason);
    }
}
