namespace Api.Data.DTOS
{
    public class GetChatRequest
    {
        public string page_id { get; set; }
        public DateTime start_date { get; set; }
        public DateTime end_date { get; set; }
        public string question { get; set; }
    }
}
