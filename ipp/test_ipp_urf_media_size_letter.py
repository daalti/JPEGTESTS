import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Color_600.urf=2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0
    +name:test_ipp_urf_media_size_letter
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_media_size_letter
        +guid:9219322e-97e7-4196-a18d-564a170548b9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_ipp_urf_media_size_letter(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'image/urf', 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
