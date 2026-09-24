/**
 * Sakhva Travel — Google Ads Daily Report → Google Sheets
 *
 * Установка:
 * 1. Google Ads → Tools → Scripts → New script
 * 2. Вставить этот код
 * 3. Заменить SPREADSHEET_URL на свою таблицу
 * 4. Run → Authorize
 * 5. Frequency: Daily, 08:00
 */

var SPREADSHEET_URL = 'ВСТАВЬ_ССЫЛКУ_НА_GOOGLE_SHEET';

function main() {
  var ss = SpreadsheetApp.openByUrl(SPREADSHEET_URL);

  // === Лист 1: Кампания по дням ===
  var sheetCampaign = getOrCreateSheet(ss, 'Campaign_Daily');
  if (sheetCampaign.getLastRow() === 0) {
    sheetCampaign.appendRow([
      'Date','Campaign','Impressions','Clicks','Cost','CTR','Avg CPC',
      'Conversions','Conv Rate','Cost/Conv','Impr Share','Top Impr Share'
    ]);
  }

  var campaignReport = AdsApp.report(
    'SELECT ' +
    'segments.date, campaign.name, metrics.impressions, metrics.clicks, ' +
    'metrics.cost_micros, metrics.ctr, metrics.average_cpc, ' +
    'metrics.conversions, metrics.conversions_from_interactions_rate, ' +
    'metrics.cost_per_conversion, metrics.search_impression_share, ' +
    'metrics.search_top_impression_percentage ' +
    'FROM campaign ' +
    'WHERE segments.date DURING YESTERDAY'
  );

  var rows = campaignReport.rows();
  while (rows.hasNext()) {
    var row = rows.next();
    sheetCampaign.appendRow([
      row['segments.date'],
      row['campaign.name'],
      row['metrics.impressions'],
      row['metrics.clicks'],
      (row['metrics.cost_micros'] / 1000000).toFixed(2),
      row['metrics.ctr'],
      (row['metrics.average_cpc'] / 1000000).toFixed(2),
      row['metrics.conversions'],
      row['metrics.conversions_from_interactions_rate'],
      (row['metrics.cost_per_conversion'] / 1000000).toFixed(2),
      row['metrics.search_impression_share'],
      row['metrics.search_top_impression_percentage']
    ]);
  }

  // === Лист 2: Ad Groups по дням ===
  var sheetAdGroup = getOrCreateSheet(ss, 'AdGroup_Daily');
  if (sheetAdGroup.getLastRow() === 0) {
    sheetAdGroup.appendRow([
      'Date','Campaign','Ad Group','Impressions','Clicks','Cost',
      'CTR','Avg CPC','Conversions','Conv Rate'
    ]);
  }

  var adGroupReport = AdsApp.report(
    'SELECT ' +
    'segments.date, campaign.name, ad_group.name, ' +
    'metrics.impressions, metrics.clicks, metrics.cost_micros, ' +
    'metrics.ctr, metrics.average_cpc, metrics.conversions, ' +
    'metrics.conversions_from_interactions_rate ' +
    'FROM ad_group ' +
    'WHERE segments.date DURING YESTERDAY'
  );

  rows = adGroupReport.rows();
  while (rows.hasNext()) {
    var row = rows.next();
    sheetAdGroup.appendRow([
      row['segments.date'],
      row['campaign.name'],
      row['ad_group.name'],
      row['metrics.impressions'],
      row['metrics.clicks'],
      (row['metrics.cost_micros'] / 1000000).toFixed(2),
      row['metrics.ctr'],
      (row['metrics.average_cpc'] / 1000000).toFixed(2),
      row['metrics.conversions'],
      row['metrics.conversions_from_interactions_rate']
    ]);
  }

  // === Лист 3: Keywords ===
  var sheetKw = getOrCreateSheet(ss, 'Keywords_Daily');
  if (sheetKw.getLastRow() === 0) {
    sheetKw.appendRow([
      'Date','Campaign','Ad Group','Keyword','Match Type',
      'Impressions','Clicks','Cost','CTR','Avg CPC',
      'Conversions','Quality Score'
    ]);
  }

  var kwReport = AdsApp.report(
    'SELECT ' +
    'segments.date, campaign.name, ad_group.name, ' +
    'ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ' +
    'metrics.impressions, metrics.clicks, metrics.cost_micros, ' +
    'metrics.ctr, metrics.average_cpc, metrics.conversions, ' +
    'ad_group_criterion.quality_info.quality_score ' +
    'FROM keyword_view ' +
    'WHERE segments.date DURING YESTERDAY'
  );

  rows = kwReport.rows();
  while (rows.hasNext()) {
    var row = rows.next();
    sheetKw.appendRow([
      row['segments.date'],
      row['campaign.name'],
      row['ad_group.name'],
      row['ad_group_criterion.keyword.text'],
      row['ad_group_criterion.keyword.match_type'],
      row['metrics.impressions'],
      row['metrics.clicks'],
      (row['metrics.cost_micros'] / 1000000).toFixed(2),
      row['metrics.ctr'],
      (row['metrics.average_cpc'] / 1000000).toFixed(2),
      row['metrics.conversions'],
      row['ad_group_criterion.quality_info.quality_score']
    ]);
  }

  // === Лист 4: Search Terms (реальные запросы) ===
  var sheetST = getOrCreateSheet(ss, 'SearchTerms_Daily');
  if (sheetST.getLastRow() === 0) {
    sheetST.appendRow([
      'Date','Campaign','Ad Group','Search Term','Keyword',
      'Impressions','Clicks','Cost','CTR','Conversions'
    ]);
  }

  var stReport = AdsApp.report(
    'SELECT ' +
    'segments.date, campaign.name, ad_group.name, ' +
    'search_term_view.search_term, segments.keyword.info.text, ' +
    'metrics.impressions, metrics.clicks, metrics.cost_micros, ' +
    'metrics.ctr, metrics.conversions ' +
    'FROM search_term_view ' +
    'WHERE segments.date DURING YESTERDAY'
  );

  rows = stReport.rows();
  while (rows.hasNext()) {
    var row = rows.next();
    sheetST.appendRow([
      row['segments.date'],
      row['campaign.name'],
      row['ad_group.name'],
      row['search_term_view.search_term'],
      row['segments.keyword.info.text'],
      row['metrics.impressions'],
      row['metrics.clicks'],
      (row['metrics.cost_micros'] / 1000000).toFixed(2),
      row['metrics.ctr'],
      row['metrics.conversions']
    ]);
  }

  Logger.log('Done. Updated 4 sheets.');
}

function getOrCreateSheet(ss, name) {
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
  }
  return sheet;
}