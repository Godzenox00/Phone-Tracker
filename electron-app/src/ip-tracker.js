const axios = require('axios');

/**
 * Track an IP address using multiple free geolocation APIs for richer data.
 * Primary: ip-api.com (no key required, 45 req/min)
 * Fallback: ipwho.is
 */
async function trackIP(ip) {
  try {
    // Primary API: ip-api.com (more reliable, more fields)
    const response = await axios.get(
      `http://ip-api.com/json/${ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query`,
      { timeout: 10000 }
    );

    if (response.data.status === 'fail') {
      throw new Error(response.data.message || 'IP lookup failed');
    }

    const d = response.data;
    return {
      success: true,
      data: {
        ip: d.query,
        continent: d.continent,
        continentCode: d.continentCode,
        country: d.country,
        countryCode: d.countryCode,
        region: d.regionName,
        regionCode: d.region,
        city: d.city,
        district: d.district || 'N/A',
        zip: d.zip,
        latitude: d.lat,
        longitude: d.lon,
        timezone: d.timezone,
        utcOffset: formatOffset(d.offset),
        currency: d.currency,
        isp: d.isp,
        org: d.org,
        as: d.as,
        asName: d.asname,
        reverse: d.reverse || 'N/A',
        isMobile: d.mobile,
        isProxy: d.proxy,
        isHosting: d.hosting,
        mapsUrl: `https://www.google.com/maps/@${d.lat},${d.lon},12z`,
      },
    };
  } catch (primaryError) {
    // Fallback to ipwho.is
    try {
      const response = await axios.get(`https://ipwho.is/${ip}`, {
        timeout: 10000,
      });
      const d = response.data;

      if (!d.success && d.success !== undefined) {
        throw new Error(d.message || 'IP lookup failed');
      }

      return {
        success: true,
        data: {
          ip: d.ip,
          type: d.type,
          continent: d.continent,
          continentCode: d.continent_code,
          country: d.country,
          countryCode: d.country_code,
          region: d.region,
          regionCode: d.region_code,
          city: d.city,
          district: 'N/A',
          zip: d.postal,
          latitude: d.latitude,
          longitude: d.longitude,
          timezone: d.timezone?.id,
          utcOffset: d.timezone?.utc,
          currency: 'N/A',
          isp: d.connection?.isp,
          org: d.connection?.org,
          as: d.connection?.asn?.toString(),
          asName: d.connection?.domain,
          reverse: 'N/A',
          isMobile: false,
          isProxy: false,
          isHosting: false,
          mapsUrl: `https://www.google.com/maps/@${d.latitude},${d.longitude},12z`,
          callingCode: d.calling_code,
          capital: d.capital,
          flag: d.flag?.emoji,
          borders: d.borders,
        },
      };
    } catch (fallbackError) {
      return {
        success: false,
        error:
          primaryError.message ||
          fallbackError.message ||
          'Failed to track IP address',
      };
    }
  }
}

/**
 * Get the user's public IP address using multiple services for reliability.
 */
async function getMyIP() {
  const services = [
    { url: 'https://api.ipify.org?format=json', extract: (d) => d.ip },
    {
      url: 'https://httpbin.org/ip',
      extract: (d) => d.origin,
    },
    {
      url: 'https://api.my-ip.io/v2/ip.json',
      extract: (d) => d.ip,
    },
  ];

  for (const service of services) {
    try {
      const response = await axios.get(service.url, { timeout: 5000 });
      const ip = service.extract(response.data);
      if (ip) {
        return { success: true, ip };
      }
    } catch {
      continue;
    }
  }

  return { success: false, error: 'Could not determine your public IP' };
}

function formatOffset(offsetSeconds) {
  if (!offsetSeconds && offsetSeconds !== 0) return 'N/A';
  const hours = Math.floor(Math.abs(offsetSeconds) / 3600);
  const minutes = Math.abs(offsetSeconds) % 3600 / 60;
  const sign = offsetSeconds >= 0 ? '+' : '-';
  return `UTC${sign}${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

module.exports = { trackIP, getMyIP };
