import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile21.urf=b920471acd77ab0c4f20b44b195d84f4d6f6e647ea394e935304b07bfb9f3a41
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_devicegray_duplex_nomedia_speci_file22
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_devicegray_duplex_nomedia_speci_file22
        +guid:312983cb-72c8-40b5-858d-a09cdb43a4c4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_devicegray_duplex_nomedia_speci_file22(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_devicegray_duplex_nomedia_speci_file22.test', 'b920471acd77ab0c4f20b44b195d84f4d6f6e647ea394e935304b07bfb9f3a41')
    outputsaver.save_output()