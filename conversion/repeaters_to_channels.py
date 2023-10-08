from functools import reduce
import typing
from loading.repeaters import Repeater
from saving.channels import RepeaterChannel


def _convert_repeater_to_channel(repeater: Repeater) -> RepeaterChannel:

    tx_frq = float(repeater.frequency) + float(repeater.offset)
    tx_frq = format(tx_frq, ".6f")

    return RepeaterChannel(
        channel_name=repeater.callsign,
        color_code=repeater.color_code,
        receive_frequency=repeater.frequency,
        transmit_frequency=tx_frq
    )


def _is_same_channel(channel_a, channel_b) -> bool:
    return channel_a.channel_name == channel_b.channel_name and channel_a.receive_frequency == channel_b.receive_frequency and channel_a.transmit_frequency == channel_b.transmit_frequency and channel_a.color_code == channel_b.color_code


def _make_unique_channels(channels: typing.List[RepeaterChannel]) -> typing.List[RepeaterChannel]:
    unique_channels = []

    for channel in channels:
        if not any(_is_same_channel(channel, other_channel) for other_channel in unique_channels):
            unique_channels.append(channel)

    return unique_channels


def convert(repeaters: typing.List[Repeater]) -> typing.List[RepeaterChannel]:

    # repeaters_dict = {repeater.id: repeater for repeater in repeaters}.values()
    # repeaters = [repeater for repeater in repeaters_dict]

    # repeaters = [
    #     repeater for repeater in repeaters if repeater.callsign == "HB9OK"]

    channels = []

    for repeater in repeaters:
        channels.append(_convert_repeater_to_channel(repeater))

    channels = _make_unique_channels(channels)

    return channels
