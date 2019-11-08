import vcr

from unittests.base import sixDKTests


class ApiWmsTests(sixDKTests):

    @vcr.use_cassette('cassettes/acknowledgement-success-response.yml')
    def testAcknowledgementSuccessResponse(self):
        """test WMS acknowledgement API success response
        for receiving an acknowledgement

        API should return acceptance message
        """
        return

    @vcr.use_cassette('cassettes/acknowledgement-success-database.yml')
    def testAcknowledgementSuccessDatabase(self):
        """test WMS acknowledgement API success database update
        for receiving an acknowledgement

        API should update Message and MessageTransmission tables with
        acknowledgement and acknowledgement response records
        """
        return

    @vcr.use_cassette('cassettes/acknowledgement-success-proxy-response.yml')
    def testAcknowledgementSuccessProxyResponse(self):
        """test WMS acknowledgement API success response
        for receiving an acknowledgement

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette('cassettes/acknowledgement-success-proxy-database.yml')
    def testAcknowledgementSuccessProxyDatabase(self):
        """test WMS acknowledgement API success database update
        for receiving an acknowledgement

        API should update Message and MessageTransmission
        tables with
        acknowledgement and acknowledgement response records
        """
        return

    def testAcknowledgementUnknownTokenResponse(self):
        """test WMS acknowledgement API unknown token response
        for receiving an acknowledgement

        API should return unknown origin wms message
        """
        return

    def testAcknowledgementUnknownTokenDatabase(self):
        """test WMS acknowledgement API unknown token response
        for receiving an acknowledgement

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette('cassettes/container-accepted-success-response.yml')
    def testContainerAcceptedSuccessResponse(self):
        """test WMS container-accepted API success response
        for receiving an container-accepted

        API should return acceptance message
        """
        return

    @vcr.use_cassette('cassettes/container-accepted-success-database.yml')
    def testContainerAcceptedSuccessDatabase(self):
        """test WMS container-accepted API success database update
        for receiving an container-accepted

        API should update Message and MessageTransmission
        tables with
        container-accepted and container-accepted response records
        """
        return

    @vcr.use_cassette(
        'cassettes/container-accepted-success-proxy-response.yml')
    def testContainerAcceptedSuccessProxyResponse(self):
        """test WMS container-accepted API success response
        for receiving an container-accepted

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette(
        'cassettes/container-accepted-success-proxy-database.yml')
    def testContainerAcceptedSuccessProxyDatabase(self):
        """test WMS container-accepted API success database update
        for receiving an container-accepted

        API should update Message and MessageTransmission tables with
        container-accepted and container-accepted response records
        """
        return

    def testContainerAcceptedUnknownTokenResponse(self):
        """test WMS container-accepted API unknown token response
        for receiving an container-accepted

        API should return unknown origin wms message
        """
        return

    def testContainerAcceptedUnknownTokenDatabase(self):
        """test WMS container-accepted API unknown token database update
        for receiving an container-accepted

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette('cassettes/print-request-success-response.yml')
    def testPrintRequestSuccessResponse(self):
        """test WMS print-request API success response
        for receiving an print-request

        API should return acceptance message
        """
        return

    @vcr.use_cassette('cassettes/print-request-success-database.yml')
    def testPrintRequestSuccessDatabase(self):
        """test WMS print-request API success database update
        for receiving an print-request

        API should update Message and MessageTransmission tables with
        print-request and print-request response records
        """
        return

    @vcr.use_cassette('cassettes/print-request-success-proxy-response.yml')
    def testPrintRequestSuccessProxyResponse(self):
        """test WMS print-request API success response
        for receiving an print-request

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette('cassettes/print-request-success-proxy-database.yml')
    def testPrintRequestSuccessProxyDatabase(self):
        """test WMS print-request API success database update
        for receiving an print-request

        API should update Message and MessageTransmission tables with
        print-request and print-request response records
        """
        return

    def testPrintRequestUnknownTokenResponse(self):
        """test WMS print-request API unknown token response
        for receiving an print-request

        API should return unknown origin wms message
        """
        return

    def testPrintRequestUnknownTokenDatabase(self):
        """test WMS print-request API unknown token database update
        for receiving an print-request

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette('cassettes/container-validation-success-response.yml')
    def testContainerValidationSuccessResponse(self):
        """test WMS container-validation API success response
        for receiving an container-validation

        API should return acceptance message
        """
        return

    @vcr.use_cassette(
        'cassettes/container-validation-success-database.yml')
    def testContainerValidationSuccessDatabase(self):
        """test WMS container-validation API success database update
        for receiving an container-validation

        API should update Message and MessageTransmission
        tables with
        container-validation and container-validation response records
        """
        return

    @vcr.use_cassette(
        'cassettes/container-validation-success-proxy-response.yml')
    def testContainerValidationSuccessProxyResponse(self):
        """test WMS container-validation API success response
        for receiving an container-validation

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette(
        'cassettes/container-validation-success-proxy-database.yml')
    def testContainerValidationSuccessProxyDatabase(self):
        """test WMS container-validation API success database update
        for receiving an container-validation

        API should update Message and MessageTransmission
        tables with
        container-validation and container-validation response records
        """
        return

    def testContainerValidationUnknownTokenResponse(self):
        """test WMS container-validation API unknown token response
        for receiving an container-validation

        API should return unknown origin wms message
        """
        return

    def testContainerValidationUnknownTokenDatabase(self):
        """test WMS container-validation API unknown token database update
        for receiving an container-validation

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette('cassettes/container-inducted-success-response.yml')
    def testContainerInductedSuccessResponse(self):
        """test WMS container-inducted API success response
        for receiving an container-inducted

        API should return acceptance message
        """
        return

    @vcr.use_cassette('cassettes/container-inducted-success-database.yml')
    def testContainerInductedSuccessDatabase(self):
        """test WMS container-inducted API success database update
        for receiving an container-inducted

        API should update Message and MessageTransmission
        tables with
        container-inducted and container-inducted response records
        """
        return

    @vcr.use_cassette(
        'cassettes/container-inducted-success-proxy-response.yml')
    def testContainerInductedSuccessProxyResponse(self):
        """test WMS container-inducted API success response
        for receiving an container-inducted

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette(
        'cassettes/container-inducted-success-proxy-database.yml')
    def testContainerInductedSuccessProxyDatabase(self):
        """test WMS container-inducted API success database update
        for receiving an container-inducted

        API should update Message and MessageTransmission
        tables with
        container-inducted and container-inducted response records
        """
        return

    def testContainerInductedUnknownTokenResponse(self):
        """test WMS container-inducted API unknown token response
        for receiving an container-inducted

        API should return unknown origin wms message
        """
        return

    def testContainerInductedUnknownTokenDatabase(self):
        """test WMS container-inducted API unknown token database update
        for receiving an container-inducted

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette('cassettes/pick-task-picked-success-response.yml')
    def testPickTaskPickedSuccessResponse(self):
        """test WMS pick-task-picked API success response
        for receiving an pick-task-picked

        API should return acceptance message
        """
        return

    @vcr.use_cassette('cassettes/pick-task-picked-success-database.yml')
    def testPickTaskPickedSuccessDatabase(self):
        """test WMS pick-task-picked API success database update
        for receiving an pick-task-picked

        API should update Message and MessageTransmission
        tables with
        pick-task-picked and pick-task-picked response records
        """
        return

    @vcr.use_cassette('cassettes/pick-task-picked-success-proxy-response.yml')
    def testPickTaskPickedSuccessProxyResponse(self):
        """test WMS pick-task-picked API success response
        for receiving an pick-task-picked

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette('cassettes/pick-task-picked-success-proxy-database.yml')
    def testPickTaskPickedSuccessProxyDatabase(self):
        """test WMS pick-task-picked API success database update
        for receiving an pick-task-picked

        API should update Message and MessageTransmission
        tables with
        pick-task-picked and pick-task-picked response records
        """
        return

    def testPickTaskPickedUnknownTokenResponse(self):
        """test WMS pick-task-picked API unknown token response
        for receiving an pick-task-picked

        API should return unknown origin wms message
        """
        return

    def testPickTaskPickedUnknownTokenDatabase(self):
        """test WMS pick-task-picked API unknown token database update
        for receiving an pick-task-picked

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette(
        'cassettes/container-picked-complete-success-response.yml')
    def testContainerPickedCompleteSuccessResponse(self):
        """test WMS container-picked-complete API success response
        for receiving an container-picked-complete

        API should return acceptance message
        """
        return

    @vcr.use_cassette(
        'cassettes/container-picked-complete-success-database.yml')
    def testContainerPickedCompleteSuccessDatabase(self):
        """test WMS container-picked-complete API success database update
        for receiving an container-picked-complete

        API should update Message and MessageTransmission
        tables with
        container-picked-complete and container-picked-complete
        response records
        """
        return

    @vcr.use_cassette(
        'cassettes/container-picked-complete-success-proxy-response.yml')
    def testContainerPickedCompleteSuccessProxyResponse(self):
        """test WMS container-picked-complete API success response
        for receiving an container-picked-complete

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette(
        'cassettes/container-picked-complete-success-proxy-database.yml')
    def testContainerPickedCompleteSuccessProxyDatabase(self):
        """test WMS container-picked-complete API success database update
        for receiving an container-picked-complete

        API should update Message and MessageTransmission
        tables with
        container-picked-complete and container-picked-complete
        response records
        """
        return

    def testContainerPickedCompleteUnknownTokenResponse(self):
        """test WMS container-picked-complete API unknown token response
        for receiving an container-picked-complete

        API should return unknown origin wms message
        """
        return

    def testContainerPickedCompleteUnknownTokenDatabase(self):
        """test WMS container-picked-complete API unknown token
        database update for receiving an container-picked-complete

        API should not update Message and MessageTransmission tables
        """
        return

    @vcr.use_cassette('cassettes/container-taken-off-success-response.yml')
    def testContainerTakenOffSuccessResponse(self):
        """test WMS container-taken-off API success response
        for receiving an container-taken-off

        API should return acceptance message
        """
        return

    @vcr.use_cassette('cassettes/container-taken-off-success-database.yml')
    def testContainerTakenOffSuccessDatabase(self):
        """test WMS container-taken-off API success database update
        for receiving an container-taken-off

        API should update Message and MessageTransmission
        tables with
        container-taken-off and container-taken-off response records
        """
        return

    @vcr.use_cassette(
        'cassettes/container-taken-off-success-proxy-response.yml')
    def testContainerTakenOffSuccessProxyResponse(self):
        """test WMS container-taken-off API success response
        for receiving an container-taken-off

        API should return a 200 OK response
        """
        return

    @vcr.use_cassette(
        'cassettes/container-taken-off-success-proxy-database.yml')
    def testContainerTakenOffSuccessProxyDatabase(self):
        """test WMS container-taken-off API success database update
        for receiving an container-taken-off

        API should update Message and MessageTransmission
        tables with
        container-taken-off and container-taken-off response records
        """
        return

    def testContainerTakenOffUnknownTokenResponse(self):
        """test WMS container-taken-off API unknown token response
        for receiving an container-taken-off

        API should return unknown origin wms message
        """
        return

    def testContainerTakenOffUnknownTokenDatabase(self):
        """test WMS container-taken-off API unknown token database update
        for receiving an container-taken-off

        API should not update Message and MessageTransmission tables
        """
        return

    def testUnknownMessageTypeResponse(self):
        """test WMS API unknown message type response

        API should return unknown message type message
        """
        return

    def testUnknownMessageTypeDatabase(self):
        """test WMS API unknown message type database update

        API should not update Message and MessageTransmission tables
        """
        return
