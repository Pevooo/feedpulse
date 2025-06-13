namespace Api.Data.DTOS
{
    public class ChatResponse
    {
        public string status { get; set; }
        public responseBody body { get; set; }

    }
    public class responseBody
    {
        public string data { get; set; }
        public int isRaster { get; set; }
    }
}
