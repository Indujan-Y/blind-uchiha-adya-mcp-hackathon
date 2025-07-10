import requests
import json
from typing import Optional, Dict, Any, List

BASE_URL = "https://appsignal.com/graphql"

class AppSignalService:
    def __init__(self, token: str):
        self.token = token
        self.base_url = BASE_URL

    def _post_graphql(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Make a GraphQL POST request to AppSignal."""
        url = f"{self.base_url}?token={self.token}"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"❌ Request failed: {response.status_code} - {response.text}")

    def search_errors(self, organization_slug: str, query_string: Optional[str] = None, namespace: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for exception errors in AppSignal using the Search GraphQL API.

        Args:
            organization_slug (str): Organization slug.
            query_string (str, optional): Search query.
            namespace (str, optional): Filter errors by namespace.

        Returns:
            dict: Exception error samples.
        """
        query = """
        query Search(
          $organizationSlug: String!
          $query: String
          $namespace: String
          $sampleType: SampleTypeEnum
        ) {
          organization(slug: $organizationSlug) {
            search(
              query: $query
              namespace: $namespace
              sampleType: $sampleType
            ) {
              ... on ExceptionSample {
                id
                time
                action
                namespace
                exception {
                  name
                  message
                }
                incident {
                  ... on ExceptionIncident {
                    number
                  }
                }
                app {
                  name
                  id
                }
              }
            }
          }
        }
        """
        variables = {
            "organizationSlug": organization_slug,
            "query": query_string,
            "namespace": namespace,
            "sampleType": "EXCEPTION"
        }
        return self._post_graphql(query, variables)

    def get_all_errors(self, app_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get all open exception incidents from AppSignal.

        Args:
            app_id (str): App ID.
            limit (int): Number of incidents to fetch.
            offset (int): Offset for pagination.

        Returns:
            dict: Exception incidents.
        """
        query = """
        query ExceptionIncidentsQuery($appId: String!, $limit: Int, $offset: Int) {
          app(id: $appId) {
            id
            exceptionIncidents(
              limit: $limit
              offset: $offset
            ) {
              id
              number
              count
              lastOccurredAt
              exceptionName
              actionNames
              namespace
              severity
            }
          }
        }
        """
        variables = {
            "appId": app_id,
            "limit": limit,
            "offset": offset
        }
        return self._post_graphql(query, variables)

    def get_incident_details(self, app_id: str, incident_number: int, sample_id: Optional[str] = None, timestamp: Optional[str] = None, timerange: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get details for a specific incident.

        Args:
            app_id (str): App ID.
            incident_number (int): Incident number.
            sample_id (str, optional): Sample ID.
            timestamp (str, optional): Timestamp.
            timerange (list, optional): Time range.

        Returns:
            dict: Incident details.
        """
        query = """
        query IncidentQuery(
          $appId: String!
          $incidentNumber: Int!
          $sampleId: String
          $timestamp: String
          $timerange: [DateTime]
        ) {
          app(id: $appId) {
            id
            incident(incidentNumber: $incidentNumber) {
              ... on ExceptionIncident {
                ...ExceptionIncident
              }
              ... on PerformanceIncident {
                ...PerformanceIncident
              }
            }
          }
        }

        fragment ExceptionIncident on ExceptionIncident {
          id
          number
          lastOccurredAt
          actionNames
          exceptionName
          state
          namespace
          firstBacktraceLine
          severity
          sample(id: $sampleId, timestamp: $timestamp, timerange: $timerange) {
            id
            time
            action
            namespace
            exception {
              name
              message
              backtrace {
                line
                method
                path
              }
            }
          }
        }

        fragment PerformanceIncident on PerformanceIncident {
          id
          number
          lastOccurredAt
          actionNames
          state
          description
          severity
          namespace
          sample(id: $sampleId, timestamp: $timestamp, timerange: $timerange) {
            id
            time
            action
            namespace
            duration
            overview {
              key
              value
            }
          }
        }
        """
        variables = {
            "appId": app_id,
            "incidentNumber": incident_number,
            "sampleId": sample_id,
            "timestamp": timestamp,
            "timerange": timerange
        }
        return self._post_graphql(query, variables)

    def get_all_incidents(self, app_id: str, limit: int = 100, offset: int = 0, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all performance incidents from AppSignal.

        Args:
            app_id (str): App ID.
            limit (int): Number of incidents to fetch.
            offset (int): Offset for pagination.
            state (str, optional): Incident state.

        Returns:
            dict: Performance incidents.
        """
        query = """
        query PerformanceIncidentsQuery(
          $appId: String!
          $limit: Int
          $offset: Int
          $state: IncidentStateEnum
          $order: IncidentOrderEnum
        ) {
          app(id: $appId) {
            id
            performanceIncidents(
              limit: $limit
              offset: $offset
              state: $state
              order: $order
            ) {
              id
              number
              actionNames
              lastOccurredAt
              notificationThreshold
              severity
              description
              namespace
            }
          }
        }
        """
        variables = {
            "appId": app_id,
            "limit": limit,
            "offset": offset,
            "state": state,
            "order": None
        }
        return self._post_graphql(query, variables) 