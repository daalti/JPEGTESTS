import logging
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.usb.device import UsbDevice
from dunetuf.metadata import get_ip
from dunetuf.udw.udw import get_underware_instance
from dunetuf.cdm import get_cdm_instance
from dunetuf.job.job import Job

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.udw = get_underware_instance(cls.ip_address)
        cls.usb_device = UsbDevice(cls.cdm, cls.udw) #type: ignore[assignment]
        cls.job = Job(cls.cdm, cls.udw) #type: ignore[assignment]

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def setup_method(self):
        if not self.usb_device.devices('frontUsb'):
            logging.info('Adding USB mock device')
            self.usb_device.add_mock_device('usbdisk1', 'UsbDisk1', 'frontUsb')

    def teardown_method(self):
        """Clean up resources after each test."""

        if self.usb_device.check_device('usbdisk1'):
            self.usb_device.remove_mock_device('usbdisk1')

        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Reset media configuration to default
        self.media.update_media_configuration(self.default_configuration)
        tear_down_output_saver(self.outputsaver)
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Test Print From Thumb drive for jpeg file with Custom size configured
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid: DUNE-218422
        +timeout: 600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:5x7in_1_1006.jpg=0fdbac1601827141ec0cb70960c57ea887089bd65b60dde7f0d4ddeb7841bc84
        +name:TestWhenPrintingJPEGFile::test_when_using_5x7in_1_1006_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_jpeg_printfromusb_custom
            +guid:398fdd83-81b8-4bc9-bf81-50fd3c8cd5f3
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=JPEG & DeviceFunction=PrintFromUsb & ConsumableSupport=Ink & MediaInputInstalled=Tray1
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    #TODO: Change job and usbdevice once the API is ready
    def test_when_using_5x7in_1_1006_file_then_succeeds(self):

        # Upload required images to simulated usb device
        self.outputsaver.operation_mode('CRC')
        usbroot = self.usb_device.get_root('usbdisk1')
        filepath = self.usb_device.upload('0fdbac1601827141ec0cb70960c57ea887089bd65b60dde7f0d4ddeb7841bc84', usbroot)

        logging.info('Creating print from USB job ticket')
        resource = {'src': {'usb': {}}, 'dest': {'print': {}}}
        ticketId = self.job.create_job_ticket(resource)

        default = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default)

        if default in media_sizes:
            self.media.tray.load(default, 'na_5x7_5x7in', self.media.MediaType.Stationery)

        mediasize = self.media.MediaSize.Custom

        resource = {
            'src': {
                'usb': {'path': filepath}
            },
            'dest': {
                'print': {
                    'mediaSource': default,
                    'mediaSize': mediasize,
                    'mediaType': self.media.MediaType.Stationery,
                }
            },
            }

        logging.info('Updating print from USB job ticket with source and destination')
        self.job.update_job_ticket(ticketId, resource)

        logging.info('Create a print job and retrieve print job id')
        jobId = self.job.create_job(ticketId)

        logging.info('Initialize and start the print job - %s', jobId)
        self.job.change_job_state(jobId, 'initialize', 'initializeProcessing')
        self.job.check_job_state(jobId, 'ready', 30)
        self.job.change_job_state(jobId, 'start', 'startProcessing')

        jobstate = self.print.wait_for_job_completion(jobId)
        expected_crc = ["0x5d91f7bc"]
        self.outputsaver.verify_output_crc(expected_crc)

        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        assert 'success' in jobstate, 'Unexpected final job state!'