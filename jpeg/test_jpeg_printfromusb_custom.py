import logging
import pytest

@pytest.fixture(autouse=True)
def setup_teardown_pdl_test(job, usbdevice):
    #override setup to prevent reset of roll length
    if not usbdevice.devices('frontUsb'):
        logging.info('Adding USB mock device')
        usbdevice.add_mock_device('usbdisk1', 'UsbDisk1', 'frontUsb')

    logging.info("Cancel all active jobs")
    job.cancel_active_jobs()
    logging.info("Wait for no active jobs")
    job.wait_for_no_active_jobs()

    yield

    if usbdevice.check_device('usbdisk1'):
        usbdevice.remove_mock_device('usbdisk1')

    logging.info("Cancel all active jobs")
    job.cancel_active_jobs()
    logging.info("Wait for no active jobs")
    job.wait_for_no_active_jobs()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Print From Thumb drive for jpeg file with Custom size configured
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-218422
    +timeout: 600
    +asset: PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:5x7in_1_1006.jpg=0fdbac1601827141ec0cb70960c57ea887089bd65b60dde7f0d4ddeb7841bc84
    +name: test_jpeg_printfromusb_custom
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_jpeg_printfromusb_custom
        +guid: 4257a200-e226-4b82-a5fe-af444d276276
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & DeviceFunction=PrintFromUsb & ConsumableSupport=Ink & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_printfromusb_custom(setup_teardown, job, usbdevice, tray, outputsaver):
    # Upload required images to simulated usb device
    outputsaver.operation_mode('CRC')
    usbroot = usbdevice.get_root('usbdisk1')
    filepath = usbdevice.upload('0fdbac1601827141ec0cb70960c57ea887089bd65b60dde7f0d4ddeb7841bc84', usbroot)

    logging.info('Creating print from USB job ticket')
    resource = {'src': {'usb': {}}, 'dest': {'print': {}}}
    ticketId = job.create_job_ticket(resource)

    default = tray.get_default_source()
    mediasize = 'custom'
    if tray.is_size_supported('na_5x7_5x7in', default):
        tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')

    resource = {
        'src': {
            'usb': {'path': filepath}
        },
        'dest': {
            'print': {
                'mediaSource': default,
                'mediaSize': mediasize,
                'mediaType': 'stationery',
            }
        },
        }

    logging.info('Updating print from USB job ticket with source and destination')
    job.update_job_ticket(ticketId, resource)

    logging.info('Create a print job and retrieve print job id')
    jobId = job.create_job(ticketId)

    logging.info('Initialize and start the print job - %s', jobId)
    job.change_job_state(jobId, 'initialize', 'initializeProcessing')
    job.check_job_state(jobId, 'ready', 30)
    job.change_job_state(jobId, 'start', 'startProcessing')

    jobstate = job.wait_for_job_completion_cdm(jobId, 120)
    expected_crc = ["0x5d91f7bc"]
    outputsaver.verify_output_crc(expected_crc)

    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    assert 'success' in jobstate, 'Unexpected final job state!'