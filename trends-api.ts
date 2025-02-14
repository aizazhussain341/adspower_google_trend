const myHeaders = new Headers();
import { argv } from "process";
myHeaders.append("accept", "application/json, text/plain, /");
myHeaders.append("accept-language", "en-US,en;q=0.9");
myHeaders.append("cookie", "_utma=10102256.736393658.1738527634.1739273681.1739520725.12; __utmc=10102256; __utmz=10102256.1739520725.12.5.utmcsr=trends.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=10102256.4.9.1739520744002; SEARCH_SAMESITE=CgQI4ZwB; HSID=AFvXLl9RS0EipqdGq; SSID=AruzLuYF5VCY4fOpm; APISID=MAwFobJL9fZeNHbk/A_911GZSTTfzxUJlY; SAPISID=yu5cXaZLVVF_NGsk/AbPjUQAplN_l7nEMI; __Secure-1PAPISID=yu5cXaZLVVF_NGsk/AbPjUQAplN_l7nEMI; __Secure-3PAPISID=yu5cXaZLVVF_NGsk/AbPjUQAplN_l7nEMI; OTZ=7937061_36_36__36; __Secure-ENID=25.SE=V3p9Y0Gb_2MGiZ385A3k3Z2X0MZ6ztyBpLhnhlF_zzlvk7sFujSwtfr6k7odTVfv6dC4rTD2_tplFHpVN7Y4nUsmgm1738vMKmf4K7TKPRLWTpij8YBobddBGUvWTnZw5izyzzq12kkHM50Xc22GOVPg9FUfXDLAAWB5bNfCmZntBD5yYxO_ZJeC_X-DZ3QCBnkMxlZM2SNyID4f9y6TOM1lR5IJSLf3gIWnZoRazOCfY0uFKs5jehUtGlijNxr7kdDiDaumCZ2Io6bP_viu95PGMpsXWqwQ7PtfsGSkts8c_JjUOno6yC86jijf7fuAEIE71-EreQjPqQNmrk7-IG_VxGPUWZb6RQy4USadpUgNwuSkTJ7aD3Gmq7gIAL2LQE-5kR6n1V0YknWUxIRblChfUAAsUnEIWQm-d3VoiAu08uJlfrcpDNh7Q8XSoLGKoOunBsFaQHiF52eHBtnECHGvFX1NAfF9ITA6p4JRdcCsdd8Uvk4c3UWWupJxblmBXixQ5yMnCkMXrsHGtM-AuQ; SID=g.a000tQjKUmuzBbemtd_2BKtEAktzlCZu_BUoG48m8pO0O__n7B60jH2UgpfKZd2z9BJyhF06GAACgYKAX8SARMSFQHGX2MicEGuQzfeztkAvqU1TA_WNBoVAUF8yKrfGm9WUpHJ7xX2_HK-2BL40076; __Secure-1PSID=g.a000tQjKUmuzBbemtd_2BKtEAktzlCZu_BUoG48m8pO0O__n7B60VteyQYozoKOT5wtcv9O1vgACgYKAQkSARMSFQHGX2Mi-6gd4oCDbUGX-Rh7pHZ5ohoVAUF8yKpNjDSpUbNdsj_O5To8S8eQ0076; __Secure-3PSID=g.a000tQjKUmuzBbemtd_2BKtEAktzlCZu_BUoG48m8pO0O__n7B60uqaLWBHAGMQ5Ee2J6tmpMAACgYKAcYSARMSFQHGX2MiV7D5ODkoOdsf72_QY-WnYxoVAUF8yKq9NVk1wUEP9HNaXseb8YOL0076; AEC=AVcja2cOGjWl13NBuzXq6fbC3uG0qjH8Gq4fnyHF12SFGA0uEhEdFhieoQ; __Secure-1PSIDTS=sidts-CjEBEJ3XV7x5Lbww-aCHbQFU6kO4UzErKQuJkWaJbV006nQ_d71ttrt1uRbJWvMDmnjoEAA; __Secure-3PSIDTS=sidts-CjEBEJ3XV7x5Lbww-aCHbQFU6kO4UzErKQuJkWaJbV006nQ_d71ttrt1uRbJWvMDmnjoEAA; NID=521=UISSsDix0p2ziCYHvEt8EFAnAQuNpw4TNqDs-8Cm5l3-NMJRJF_qUoKeOW8Un_SNjlw9qwVIQRSxQVUzlvOEeqlUI_sXzbZSAvCz-kblQGCeXRlJrFGC6TdeG6fVQpjji526oOfALujslejX-kaQeZQ6ynfPymt6OGA_Md6Dm--ol31DOkr-FXm4twYqF0cTxVpa_p7VhH_Le6p-Na1tYcJ101Bwzc5ZOSkXfpt_ELSERDXkFRYMen0pLwYwL6r3Xw9q1tvCcirf95FPXDJOAHv8jUUelJnImZL-scL_I2pVPnSWxltjn7SQRPWkXNZ_ZI8My2j-n0ttCAV62czLnPY3dWsKMn_gm_xUCSaxglU6Rugks_kErISouNm134sTGhzQqT-1L2eyJ6-bLzmZMIWQVRaHOoD0z-bk64UIvr4dGSLOzXc-WPCbrcXJ5d_32extoKvLX2qrHzIA-Mjy4SlP_gAWgdj5Pg_pTuYIjVpfx75nv1pH42vKCVUBW_GthmREaDVR92EMxp9vCF_5OdzvWzJ8MNHX2hK99V_7NuBNupPRZwDSkwILV7H55kFjoEBddYuP5AMU6dtQEFoEruZQj677yxFU3tAKcZmENMqPrcgDmFBGSTnIXEYUKMAu_uKkC09Q49hswc3pSNc8qjdWGulq5R3BpVbRNMYCLi13avEUKGPVeKC_omtXhbRvK4Y7jtyBg9s8kHKGUMDtWNdu2d329lR4T7It0GLb_oVKFMXWFw; _gid=GA1.3.215453821.1739520716; _ga=GA1.3.736393658.1738527634; _ga_VWZPXDNJJB=GS1.1.1739520715.16.1.1739520775.0.0.0; SIDCC=AKEyXzVFMuNupDijRHgfZQyg_Ip9OUwW2qVkMQJRjzdUzeZROr6VTQ-DaF36Pmy5G3UkkcgXvvk; __Secure-1PSIDCC=AKEyXzXZ8giaiujlm2JdMx1jkjOC3_aVoAtGXfFmu6KwJdKr1IpI0tMUiVrmYLkEligb-KX4qMI; __Secure-3PSIDCC=AKEyXzVU1dZC2LFwAsogKmVU8cxLfv5RKD2sL-ceuKUVNH8cq22y6-3ubDlhplm1JH06N6GJnGUk");
myHeaders.append("priority", "u=1, i");
myHeaders.append("referer", "https://trends.google.com/trends/explore?date=2024-01-14%202025-02-14&geo=PK&q=facebook&hl=en");
myHeaders.append("sec-ch-ua", "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"");
myHeaders.append("sec-ch-ua-arch", "\"x86\"");
myHeaders.append("sec-ch-ua-bitness", "\"64\"");
myHeaders.append("sec-ch-ua-form-factors", "\"Desktop\"");
myHeaders.append("sec-ch-ua-full-version", "\"131.0.6778.108\"");
myHeaders.append("sec-ch-ua-full-version-list", "\"Google Chrome\";v=\"131.0.6778.108\", \"Chromium\";v=\"131.0.6778.108\", \"Not_A Brand\";v=\"24.0.0.0\"");
myHeaders.append("sec-ch-ua-mobile", "?0");
myHeaders.append("sec-ch-ua-model", "\"\"");
myHeaders.append("sec-ch-ua-platform", "\"Linux\"");
myHeaders.append("sec-ch-ua-platform-version", "\"5.15.0\"");
myHeaders.append("sec-ch-ua-wow64", "?0");
myHeaders.append("sec-fetch-dest", "empty");
myHeaders.append("sec-fetch-mode", "cors");
myHeaders.append("sec-fetch-site", "same-origin");
myHeaders.append("user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36");
myHeaders.append("x-client-data", "CKK1yQEIkbbJAQiltskBCIqSygEIqZ3KAQipgcsBCJWhywEIm/7MAQiHoM0BCP7azgEIydzOAQiC3c4BCI/fzgEY9snNARj11s4B");

interface RawTimelineItem {
  formattedAxisTime: string;
  formattedValue: string[];
}

interface TransformedTimelineItem {
  formattedAxisTime: string;
  formattedValue: string;
}

interface InputData {
  default: {
    timelineData: RawTimelineItem[];
  };
}

function transformTimelineData(input: InputData): TransformedTimelineItem[] {
  return input.default.timelineData.map(item => ({
    formattedAxisTime: item.formattedAxisTime,
    formattedValue: item.formattedValue[0]
  }));
}

const requestOptions: RequestInit = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
};

const startDate = "2024-01-14";
const endDate = "2025-02-14";
const keyword = argv[2];
const country = "PK";
const tz = -300;
const url = `https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=${tz}&req=%7B%22time%22:%22${startDate}+${endDate}%22,%22resolution%22:%22WEEK%22,%22locale%22:%22en-US%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%22country%22:%22${country}%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22${keyword}%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D,%22userConfig%22:%7B%22userType%22:%22USER_TYPE_LEGIT_USER%22%7D%7D&token=APP6_UEAAAAAZ7BMh8d1bjUZECoh6ljZqZXjauaBdSsp&tz=${tz}`;
console.log(url)

fetch(url, requestOptions)
    .then(response => response.text())
    .then(text => {
        const cleanedText = text.replace(")]}',", "");
        console.log(cleanedText)
        return JSON.parse(cleanedText);
    })
    .then(data => {
        // Stringify the transformed data and write it as a single line
        console.log(JSON.stringify(transformTimelineData(data)));
    })
    .catch(error => {
        // Write errors to stderr
        console.log("Error ======> ")
        console.log({ error: error });
    });
