import pytest
import logging

from dunetuf.print.output.intents import Intents,  Plex, MediaSource, ContentOrientation, PlexBinding, MediaSize


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value sides_two_sided_short_edge
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_pdl_intent_ipp_pdf_sides_two_sided_short_edge
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_sides_two_sided_short_edge
        +guid:590280f7-7753-4e33-8b86-9d453a860e30
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & Duplexer=True & MediaSizeSupported=na_letter_8.5x11in & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_sides_two_sided_short_edge(setup_teardown, printjob, outputsaver, outputverifier, udw):
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/pdf', 'sides': 'two-sided-short-edge', 'media-source': 'tray-1', 'orientation-requested': 4, 'copies':3, 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 3)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    print(Current_crc_value)
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"