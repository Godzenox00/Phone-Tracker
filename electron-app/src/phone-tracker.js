const {
  parsePhoneNumber,
  isValidPhoneNumber,
  isPossiblePhoneNumber,
  getCountryCallingCode,
  getExampleNumber,
  AsYouType,
} = require('libphonenumber-js');

/**
 * Track and analyze a phone number using Google's libphonenumber (JS port).
 * This is the same library used by Android and Google services - more accurate
 * than the Python phonenumbers package.
 */
function trackPhone(phoneNumber, defaultRegion = 'US') {
  try {
    const parsed = parsePhoneNumber(phoneNumber, defaultRegion);

    if (!parsed) {
      return { success: false, error: 'Could not parse phone number' };
    }

    const valid = parsed.isValid();
    const possible = parsed.isPossible();
    const numberType = parsed.getType() || 'UNKNOWN';
    const country = parsed.country || defaultRegion;

    // Format the number in various ways
    const international = parsed.formatInternational();
    const national = parsed.formatNational();
    const e164 = parsed.format('E.164');
    const uri = parsed.getURI();

    // Type descriptions
    const typeMap = {
      MOBILE: 'Mobile',
      FIXED_LINE: 'Fixed Line',
      FIXED_LINE_OR_MOBILE: 'Fixed Line or Mobile',
      TOLL_FREE: 'Toll Free',
      PREMIUM_RATE: 'Premium Rate',
      SHARED_COST: 'Shared Cost',
      VOIP: 'VoIP',
      PERSONAL_NUMBER: 'Personal Number',
      PAGER: 'Pager',
      UAN: 'Universal Access Number',
      VOICEMAIL: 'Voicemail',
      UNKNOWN: 'Unknown',
    };

    // Country names
    const regionNames = new Intl.DisplayNames(['en'], { type: 'region' });
    let countryName = 'Unknown';
    try {
      countryName = regionNames.of(country);
    } catch {
      countryName = country;
    }

    let callingCode = '';
    try {
      callingCode = '+' + getCountryCallingCode(country);
    } catch {
      callingCode = 'N/A';
    }

    return {
      success: true,
      data: {
        country: countryName,
        countryCode: country,
        callingCode: callingCode,
        nationalNumber: parsed.nationalNumber,
        internationalFormat: international,
        nationalFormat: national,
        e164Format: e164,
        uri: uri,
        type: typeMap[numberType] || numberType,
        isValid: valid,
        isPossible: possible,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: error.message || 'Failed to parse phone number. Use format: +1234567890',
    };
  }
}

module.exports = { trackPhone };
