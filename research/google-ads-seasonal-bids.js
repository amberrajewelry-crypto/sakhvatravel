/**
 * Google Ads Script: Seasonal Bid Adjustments for Sakhva Travel
 *
 * Автоматически корректирует ставки по сезонам.
 * Запускать ежедневно в Google Ads → Tools → Scripts.
 *
 * Сезоны:
 *   Апрель-Июнь:   +20% (начало сезона)
 *   Июль-Сентябрь: +30% (пик сезона)
 *   Октябрь:       +10% (бархатный сезон)
 *   Ноябрь-Февраль: -20% (низкий сезон)
 *   Март:           0% (межсезонье)
 *   20 дек — 10 янв: +25% (новогодние каникулы, перекрывает зимний -20%)
 */

var CAMPAIGN_NAMES = [
  'Sakhva_Search_Flagships',
  'Sakhva_Search_Guide',
  'Sakhva_Search_General',
  'Sakhva_Search_Competitors'
];

function main() {
  var today = new Date();
  var month = today.getMonth() + 1; // 1-12
  var day = today.getDate();

  var modifier = getSeasonalModifier(month, day);
  var label = getSeasonLabel(month, day);

  Logger.log('Date: ' + today.toISOString().slice(0, 10));
  Logger.log('Season: ' + label);
  Logger.log('Bid modifier: ' + (modifier > 0 ? '+' : '') + modifier + '%');

  // Mobile device bid = seasonal + 20% base mobile boost
  var mobileMod = 1.20 * (1 + modifier / 100);
  var mobilePercent = Math.round((mobileMod - 1) * 100);

  for (var i = 0; i < CAMPAIGN_NAMES.length; i++) {
    var campaignIterator = AdsApp.campaigns()
      .withCondition("Name = '" + CAMPAIGN_NAMES[i] + "'")
      .get();

    while (campaignIterator.hasNext()) {
      var campaign = campaignIterator.next();

      // Desktop bid modifier (seasonal only)
      campaign.targeting().platforms().desktop().setBidModifier(1 + modifier / 100);

      // Mobile bid modifier (seasonal + 20% base)
      campaign.targeting().platforms().mobile().setBidModifier(mobileMod);

      // Tablet -10% base + seasonal
      var tabletMod = 0.90 * (1 + modifier / 100);
      campaign.targeting().platforms().tablet().setBidModifier(tabletMod);

      Logger.log(campaign.getName() + ': desktop ' + modifier + '%, mobile +' + mobilePercent + '%, tablet ' + Math.round((tabletMod - 1) * 100) + '%');
    }
  }
}

function getSeasonalModifier(month, day) {
  // New Year override: Dec 20 - Jan 10
  if ((month === 12 && day >= 20) || (month === 1 && day <= 10)) {
    return 25;
  }

  if (month >= 4 && month <= 6) return 20;   // Apr-Jun
  if (month >= 7 && month <= 9) return 30;   // Jul-Sep
  if (month === 10) return 10;               // Oct
  if (month >= 11 || month <= 2) return -20; // Nov-Feb
  return 0;                                   // Mar
}

function getSeasonLabel(month, day) {
  if ((month === 12 && day >= 20) || (month === 1 && day <= 10)) return 'New Year Peak';
  if (month >= 4 && month <= 6) return 'Early Season';
  if (month >= 7 && month <= 9) return 'Peak Season';
  if (month === 10) return 'Velvet Season';
  if (month >= 11 || month <= 2) return 'Low Season';
  return 'Shoulder Season';
}
