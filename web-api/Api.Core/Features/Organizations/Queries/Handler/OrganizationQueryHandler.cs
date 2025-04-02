using Api.Core.Bases;
using Api.Core.Features.Organizations.Queries.Models;
using Api.Core.Features.Organizations.Queries.Responses;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;
using System.Text;
using System.Text.Json;

namespace Api.Core.Features.Organizations.Queries.Handler
{

    public class OrganizationQueryHandler : ResponseHandler, IRequestHandler<GetOrganizationListQuery, Response<List<GetOrganizationResponse>>>
                            , IRequestHandler<GetOrganizationQuery, Response<GetOrganizationResponse>>
                            , IRequestHandler<GetOrganizationStatusQuery, Response<OrganizationStatusResponse>>
    {
        #region Fields
        private readonly IOrganizationService _organizationService;
        private readonly IMapper _mapper;
        private readonly HttpClient _httpClient;
        #endregion
        #region Constructor
        public OrganizationQueryHandler(IOrganizationService organizationService, IMapper mapper, HttpClient httpClient)
        {
            _organizationService = organizationService;
            _mapper = mapper;
            _httpClient = httpClient;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<List<GetOrganizationResponse>>> Handle(GetOrganizationListQuery request, CancellationToken cancellationToken)
        {
            var organizations = await _organizationService.GetOrganizationsByUseridAsync(request.UserId);
            var response = organizations.Select(o => new GetOrganizationResponse
            {
                Name = o.Name,
                Description = o.Description,
                FacebookId = o.FacebookId,
                PageAccessToken = o.PageAccessToken
            }).ToList();

            return Success(response);
        }

        public async Task<Response<GetOrganizationResponse>> Handle(GetOrganizationQuery request, CancellationToken cancellationToken)
        {
            var organization = await _organizationService.GetOrganizationByIdAsync(request.OrganizationId);
            var response = new GetOrganizationResponse
            {
                Name = organization.Name,
                Description = organization.Description,
                FacebookId = organization.FacebookId,
                PageAccessToken = organization.PageAccessToken
            };
            return Success(response);
        }

        public async Task<Response<OrganizationStatusResponse>> Handle(GetOrganizationStatusQuery request, CancellationToken cancellationToken)
        {
            var url = "https://feedpulse.francecentral.cloudapp.azure.com/report";

            var requestBody = new
            {
                page_id = request.FacebookId,
                start_date = request.start_date.ToString("yyyy-MM-ddTHH:mm:ss.fff"), // ISO 8601
                end_date = request.end_date.ToString("yyyy-MM-ddTHH:mm:ss.fff"),   // ISO 8601


            };

            var jsonContent = new StringContent(
                JsonSerializer.Serialize(requestBody),
                Encoding.UTF8,
            "application/json"
            );

            var response = await _httpClient.PostAsync(url, jsonContent);
            if (!response.IsSuccessStatusCode)
            {
                throw new Exception($"Error: {response.StatusCode} - {await response.Content.ReadAsStringAsync()}");
            }

            var responseContent = await response.Content.ReadAsStringAsync();
            using var doc = JsonDocument.Parse(responseContent);
            var root = doc.RootElement;

            // Extract the "body" property
            if (!root.TryGetProperty("body", out JsonElement body))
            {
                throw new Exception("Invalid response: 'body' property missing.");
            }

            // Extract "goals"
            var goals = body.GetProperty("goals").EnumerateArray().Select(x => x.GetString()).ToList();

            // Extract "chart_rasters"
            var chartRasters = body.GetProperty("chart_rasters").EnumerateArray().Select(x => x.GetString()).ToList();

            var result = new OrganizationStatusResponse
            {
                Graphs = chartRasters,
            };
            return Success<OrganizationStatusResponse>(result);


        }
        #endregion
    }
}
