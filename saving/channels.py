import csv
from enum import Enum
from pathlib import Path
import typing

HEADER = ["No.", "Channel Name", "Receive Frequency", "Transmit Frequency", "Channel Type", "Transmit Power",
          "Band Width", "CTCSS/DCS Decode", "CTCSS/DCS Encode", "Contact", "Contact Call Type", "Radio ID",
          "Busy Lock/TX Permit", "Squelch Mode", "Optional Signal", "DTMF ID", "2Tone ID", "5Tone ID", "PTT ID",
          "Color Code", "Slot", "Scan List", "Receive Group List", "TX Prohibit", "Reverse", "Simplex TDMA",
          "TDMA Adaptive", "AES Encryption", "Digital Encryption", "Call Confirmation", "Talk Around", "Work Alone",
          "Custom CTCSS", "2TONE Decode", "Ranging", "Through Mode", "Digi APRS RX", "Analog APRS PTT Mode",
          "Digital APRS PTT Mode", "APRS Report Type", "Digital APRS Report Channel", "Correct Frequency[Hz]",
          "SMS Confirmation", "DMR MODE", "Exclude channel from roaming"]

TRAILER_VFO_A = ["4001", "Channel VFO A", "439.17500", "431.57500", "A-Analog", "Mid", "12.5K", "Off", "Off", "Local",
                 "Group Call", "HB9HTX", "Off", "Carrier", "Off", "1", "1", "1", "Off", "2", "2", "Schweiz",
                 "Group List 1", "Off", "Off", "Off", "Off", "Normal Encryption", "Off", "Off", "Off", "Off", "131.8",
                 "1", "Off", "Off", "Off", "Off", "Off", "Off", "1", "0", "Off", "0", "0"]

TRAILER_VFO_B = ["4002", "Channel VFO B", "145.60000", "145.60000", "A-Analog", "High", "12.5K", "Off", "Off", "Local",
                 "Group Call", "HB9HTX", "Off", "Carrier", "Off", "1", "1", "1", "Off", "1", "1", "Schweiz",
                 "Group List 1", "Off", "Off", "Off", "Off", "Normal Encryption", "Off", "Off", "Off", "Off", "131.8",
                 "1", "Off", "Off", "Off", "Off", "Off", "Off", "1", "0", "Off", "0", "0"]


class ChannelType(str, Enum):
    D_DIGITAL = "D-Digital"
    A_ANALOG = "A-Analog"
    AD_TX_A = "A+D TX A"
    DA_TX_D = "D+A TX D"


class TransmitPower(str, Enum):
    SMALL = "Small"
    LOW = "Low"
    MID = "Mid"
    HIGH = "High"


class BandWidth(str, Enum):
    BW_12k5 = "12.5k"
    BW_25k = "25k"


class TxPermit(str, Enum):
    ALWAYS = "Always"
    CHANNEL_FREE = "ChannelFree"
    DIFFERENT_COLOR_CODE = "Different Color Code"
    SAME_COLOR_CODE = "Same Color Code"


class SquelchMode(str, Enum):
    CARRIER = "Carrier"
    CTCSS_DCS = "CTCSS/DCS"


class RepeaterChannel(typing.NamedTuple):
    channel_name: str
    receive_frequency: str
    transmit_frequency: str
    color_code: int


class _Channel(typing.NamedTuple):
    id: int
    channel_type: ChannelType
    transmit_power: TransmitPower
    band_width: BandWidth
    ctcss_dcs_decode: str
    ctcss_dcs_encode: str
    contact: str
    contact_call_type: str
    radio_id: str
    busy_lock_tx_permit: TxPermit
    squelch_mode: SquelchMode
    optional_signal: str
    dtmf_id: str
    two_tone_id: str
    five_tone_id: str
    ptt_id: str
    slot: str
    scan_list: str
    receive_group_list: str
    tx_prohibit: str
    reverse: str
    simplex_tdma: str
    tdma_adaptive: str
    aes_encryption: str
    digital_encryption: str
    call_confirmation: str
    talk_around: str
    work_alone: str
    custom_ctcss: str
    two_tone_decode: str
    ranging: str
    through_mode: str
    digi_aprs_rx: str
    analog_aprs_ptt_mode: str
    digital_aprs_ptt_mode: str
    aprs_report_type: str
    digital_aprs_report_channel: str
    correct_frequency: str
    sms_confirmation: str
    dmr_mode: str
    exclude_channel_from_roaming: str
    repeater_channel: RepeaterChannel


def _create_channel_list(repeater_channels: typing.List[RepeaterChannel]) -> typing.List[_Channel]:
    channels = []

    channel_id = 1
    for channel in repeater_channels:
        channels.append(_Channel(
            id=channel_id,
            channel_type=ChannelType.D_DIGITAL,
            transmit_power=TransmitPower.HIGH,
            band_width=BandWidth.BW_12k5,
            ctcss_dcs_decode="Off",
            ctcss_dcs_encode="Off",
            contact="CH Deutsch",
            contact_call_type="Group Call",
            radio_id="HB9HTX",
            busy_lock_tx_permit=TxPermit.ALWAYS,
            squelch_mode=SquelchMode.CARRIER,
            optional_signal="Off",
            dtmf_id="1",
            two_tone_id="1",
            five_tone_id="1",
            ptt_id="Off",
            slot="2",
            scan_list="Schweiz",
            receive_group_list="Group List 1",
            tx_prohibit="Off",
            reverse="Off",
            simplex_tdma="Off",
            tdma_adaptive="Off",
            aes_encryption="Normal Encryption",
            digital_encryption="Off",
            call_confirmation="Off",
            talk_around="Off",
            work_alone="Off",
            custom_ctcss="251.1",
            two_tone_decode="1",
            ranging="Off",
            through_mode="Off",
            digi_aprs_rx="Off",
            analog_aprs_ptt_mode="Off",
            digital_aprs_ptt_mode="Off",
            aprs_report_type="Off",
            digital_aprs_report_channel="1",
            correct_frequency="0",
            sms_confirmation="Off",
            dmr_mode="0",
            exclude_channel_from_roaming="0",
            repeater_channel=channel
        ))
        channel_id = channel_id + 1

    return channels


def write_to_file(filename: Path, channels: typing.List[RepeaterChannel]):
    print(f"Exporting {len(channels)} channels to {filename}")

    channels = _create_channel_list(channels)

    with open(filename, 'w', newline='', encoding="latin-1") as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='\"', quoting=csv.QUOTE_ALL)
        writer.writerow(HEADER)

        channels_written = 0
        for channel in channels:
            try:
                writer.writerow([
                    channel.id,
                    channel.repeater_channel.channel_name,
                    channel.repeater_channel.receive_frequency,
                    channel.repeater_channel.transmit_frequency,
                    channel.channel_type,
                    channel.transmit_power,
                    channel.band_width,
                    channel.ctcss_dcs_decode,
                    channel.ctcss_dcs_encode,
                    channel.contact,
                    channel.contact_call_type,
                    channel.radio_id,
                    channel.busy_lock_tx_permit,
                    channel.squelch_mode,
                    channel.optional_signal,
                    channel.dtmf_id,
                    channel.two_tone_id,
                    channel.five_tone_id,
                    channel.ptt_id,
                    channel.repeater_channel.color_code,
                    channel.slot,
                    channel.scan_list,
                    channel.receive_group_list,
                    channel.tx_prohibit,
                    channel.reverse,
                    channel.simplex_tdma,
                    channel.tdma_adaptive,
                    channel.aes_encryption,
                    channel.digital_encryption,
                    channel.call_confirmation,
                    channel.talk_around,
                    channel.work_alone,
                    channel.custom_ctcss,
                    channel.two_tone_decode,
                    channel.ranging,
                    channel.through_mode,
                    channel.digi_aprs_rx,
                    channel.analog_aprs_ptt_mode,
                    channel.digital_aprs_ptt_mode,
                    channel.aprs_report_type,
                    channel.digital_aprs_report_channel,
                    channel.correct_frequency,
                    channel.sms_confirmation,
                    channel.dmr_mode,
                    channel.exclude_channel_from_roaming,
                ])
                channels_written = channels_written + 1
            except Exception as e:
                print(f"Channel '{channel}' could not be written: \n\t{e}")

        print(f"Exported {channels_written} channels")

        writer.writerow(TRAILER_VFO_A)
        writer.writerow(TRAILER_VFO_B)
