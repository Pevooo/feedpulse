using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace Api.Data.DTOS
{
    public class ReportResponse
	{
		[JsonPropertyName("body")]
		public Body Body { get; set; }
		[JsonPropertyName("status")]
		public string Status { get; set; }
	}

	public class Body
	{
		[JsonPropertyName("chart_rasters")]
		public List<string> ChartRasters { get; set; }
		[JsonPropertyName("goals")]
		public List<string> Goals { get; set; }
		[JsonPropertyName("metrics")]
		public Metrics Metrics { get; set; }
		[JsonPropertyName("summary")]
		public string Summary { get; set; }
	}

	public class Metrics
	{
		[JsonPropertyName("most_freq_sentiment_per_topic")]
		public Dictionary<string, string> MostFreqSentimentPerTopic { get; set; }

		[JsonPropertyName("most_freq_topic_per_sentiment")]
		public Dictionary<string, string> MostFreqTopicPerSentiment { get; set; }

		[JsonPropertyName("sentiment_counts")]
		public Dictionary<string, int> SentimentCounts { get; set; }

		[JsonPropertyName("top_5_topics")]
		public Dictionary<string, int> Top5Topics { get; set; }

		[JsonPropertyName("topic_counts")]
		public Dictionary<string, int> TopicCounts { get; set; }
	}
}
