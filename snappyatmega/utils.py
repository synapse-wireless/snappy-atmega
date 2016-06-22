# (c) Copyright 2011-2016, Synapse Wireless, Inc.
"""ATmega128RFA1 misc tools library
Other tools that don't fit in the other parts of the library can be found here.
"""


def adcRefSelect(voltageX10):
    """Allows you to select the ADC reference voltage of 1.5, 1.6, or 1.8 volts.
    Since SNAPpy only has integers, ask for 10X the desired reference voltage value."""
    ADMUX = 0x7C
    ADCSRA = 0x7A
    if voltageX10 == 15:
        select = 0x02
    elif voltageX10 == 16:
        select = 0x03
    elif voltageX10 == 18:
        select = 0x01
    else:
        return  # ignore invalid requests

    adcmux = peek(ADMUX)
    adcmux &= 0x3f  # strip off top two bits
    adcmux |= (select << 6)
    poke(ADMUX, adcmux)
    # The above does not take effect until ADC toggled off/on
    adccon = peek(ADCSRA)
    adccon &= 0x7f
    poke(ADCSRA, adccon)
    adccon |= 0x80
    poke(ADCSRA, adccon)
