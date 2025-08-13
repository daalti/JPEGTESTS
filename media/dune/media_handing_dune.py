import logging
from typing import Any, Dict
from dunetuf.media.media_handling import MediaHandling
import time

class MediaHandlingDune(MediaHandling):
    """
    Media Handling implementation for the DUNE platform.
    Executes CDM calls for alerts, configuration, and capabilities.
    """

    def get_alerts(self) -> Dict[str, Any]:
        """
        GET /cdm/mediaHandling/v1/alerts
        Retrieve the list of current media handling alerts from the DUNE device.

        Returns:
            Dict[str, Any]: JSON deserialized response containing active alerts.
        """
        logging.info("Fetching media handling alerts (DUNE)")
        return self._cdm.get(self._cdm.CDM_MEDIAHANDLING_ALERTS)

    def put_alert_action(self, alert_id: str, action: str) -> None:
        """
        PUT /cdm/mediaHandling/v1/alerts/{alertId}/action
        Acknowledge or respond to a specific alert on the device.

        Args:
            alert_id (str): Identifier of the alert to act upon.
            action (str): Action string (e.g., 'ok', 'cancel', 'modify').
        """
        logging.info("Sending alert action '%s' for alert %s (DUNE)", action, alert_id)
        self._cdm.put(
            f"{self._cdm.CDM_MEDIAHANDLING_ALERTS}/{alert_id}/action",
            {"action": action}
        )

    def get_configuration(self) -> Dict[str, Any]:
        """
        GET /cdm/mediaHandling/v1/configuration
        Retrieve the current media handling configuration settings from the DUNE device.

        Returns:
            Dict[str, Any]: JSON deserialized response containing configuration details.
        """
        logging.info("Fetching media handling configuration (DUNE)")
        return self._cdm.get(self._cdm.CDM_MEDIAHANDLING_CONFIGURATION)

    def update_configuration(self, payload: Dict[str, Any]) -> None:
        """
        PATCH /cdm/mediaHandling/v1/configuration
        Apply a partial update to the device’s media handling configuration.

        Args:
            payload (Dict[str, Any]): A dictionary of fields to update.
        """
        logging.info("Updating media handling configuration (DUNE): %s", payload)
        self._cdm.patch(self._cdm.CDM_MEDIAHANDLING_CONFIGURATION, payload)

    def get_capabilities(self) -> Dict[str, Any]:
        """
        GET /cdm/mediaHandling/v1/capabilities
        Retrieve the media handling capabilities supported by the DUNE device.

        Returns:
            Dict[str, Any]: JSON deserialized response containing device capabilities.
        """
        logging.info("Fetching media handling capabilities (DUNE)")
        return self._cdm.get(self._cdm.CDM_MEDIAHANDLING_CAPABILITIES)
    
    def get_alerts_by_category(self, category='any'):
        """Get and return media handling alert list."""
        alerts = self.get_alerts().get('alerts', [])
        logging.debug('Media handling alerts: %s', alerts)

        alerts = [alert for alert in alerts if alert.get('category') == category or category == 'any']
        return alerts
    
    def wait_for_alerts(self, category='any', timeout=15):
        """Wait until a specific category of media alert is observed."""
        
        logging.info('Waiting for media handling alert of category: %s', category)        

        time_step = 0.5
        time_elapsed = 0

        while time_elapsed <= timeout:
            time.sleep(time_step)
            time_elapsed += time_step

            alerts = self.get_alerts_by_category(category)
            logging.info('Expected alert category: %s, timeElapsed: %.1fs', category, time_elapsed)
            if alerts:
                logging.info('Expected alert category: %s, alerts raised: %s', category, alerts)
                return alerts

        raise TimeoutError('Timeout waiting media handling alert!')

    def alert_action(self, category, response):
        """Check the Flow Category against the one returned by cdm."""
        alerts = self.get_alerts_by_category(category)
        response_data = {'selectedAction':  response}
        response_created = False
        for alert in alerts:
            if alert["category"] == 'sizeType' and category == 'sizeType':
                data = alert.get('data')
                for item in data:
                    if(item.get('propertyPointer') == '/currentMediaSource'):
                        media_source = item.get('value', {}).get('seValue') 
                        response_data = {"selectedAction": response, "mediaSourceId": media_source}
                        print("\n response data: " + str(response_data))
                        response_created = True
                        break
                if response_created:
                    break
        alerts = self.get_alerts_by_category(category)
        for alert in alerts:
            action_urls = alert.get('actions').get('links')
            action_url = [url.get('href') for url in action_urls][0]

            result = self._cdm.put_raw(action_url, response_data)
            assert result.status_code == 200