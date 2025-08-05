import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file 
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191063
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Mixed_Page_Size_Region_4p_v3.pdf=e5bc714378e67161a25aa8f23dec3472dc40c5cb70473915bb55cb76e813f662
    +test_classification:System
    +name:test_pdl_airprint_mac_scaling_mediasize_letter
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_scaling_mediasize_letter
        +guid:674458ff-ed92-4532-ab1e-01b8c8f5bf6e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & MediaInputInstalled=Tray1
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_scaling_mediasize_letter(setup_teardown, printjob, udw, outputsaver):
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/pdf', 'scaling': 'auto', 'copies':1, 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    printjob.ipp_print(ipp_test_file, 'e5bc714378e67161a25aa8f23dec3472dc40c5cb70473915bb55cb76e813f662')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"