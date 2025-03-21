using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Data.Entities
{
	public class Reports
	{
		public int Id { get; set; }
		public DateTime CreatedAt { get; set; }
		public string InsightsData { get; set; }
	}
}
