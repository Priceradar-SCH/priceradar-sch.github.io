---
name: Price Radar
description: Light operate dashboard where the own shop price is the bench and every marketplace row is a gap against it.
colors:
  accent: "#5b5bf6"
  accent-wash: "#ececfe"
  accent-lift: "#7c5cff"
  undercut: "#e5484d"
  undercut-wash: "#fdecec"
  undercut-ink: "#9f1239"
  ahead: "#1f7a45"
  ahead-wash: "#e6f6ec"
  ahead-ink: "#166534"
  warning: "#8a5a08"
  warning-wash: "#fdf3e1"
  ground: "#f7f7f8"
  card: "#ffffff"
  ink: "#0b0b0f"
  mute: "#5c6370"
  line: "#e7e7eb"
  soft: "#f1f1f4"
  scrim: "rgba(8,8,14,.45)"
  zalando: "#ff6900"
  otto: "#d4002a"
  galeria: "#2a6ad8"
  amazon: "#e07a00"
  ebay: "#0064d2"
  about-you: "#111111"
  kaufland: "#e10915"
  series-unknown: "#5c6570"
typography:
  display:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "26px"
    fontWeight: 650
    lineHeight: 1.45
    letterSpacing: "-0.02em"
    fontFeature: "\"cv11\", \"ss01\""
  headline:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "22px"
    fontWeight: 680
    lineHeight: 1.45
    letterSpacing: "-0.02em"
    fontFeature: "\"cv11\", \"ss01\""
  title:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "13.5px"
    fontWeight: 620
    lineHeight: 1.3
    letterSpacing: "normal"
    fontFeature: "\"cv11\", \"ss01\""
  body:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "normal"
    fontFeature: "\"cv11\", \"ss01\""
  label:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "12.5px"
    fontWeight: 550
    lineHeight: 1.45
    letterSpacing: "normal"
    fontFeature: "\"cv11\", \"ss01\""
rounded:
  badge: "6px"
  segment: "7px"
  link: "8px"
  control: "9px"
  mark: "10px"
  inset: "12px"
  card: "16px"
  pill: "99px"
spacing:
  row: "4px"
  tight: "8px"
  stack: "10px"
  pad: "12px"
  card: "14px"
  block: "16px"
  gutter: "28px"
components:
  button:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "34px"
  button-hover:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 12px"
    height: "34px"
  button-icon:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0"
    width: "34px"
    height: "34px"
  segment:
    backgroundColor: "{colors.soft}"
    rounded: "{rounded.control}"
    padding: "2px"
  segment-on:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.segment}"
    padding: "5px 9px"
  select:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 10px"
    height: "34px"
  kpi:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "16px 18px"
  card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "14px"
  shop-block:
    backgroundColor: "{colors.accent-wash}"
    textColor: "{colors.ink}"
    rounded: "{rounded.inset}"
    padding: "10px 12px"
  pill-undercut:
    backgroundColor: "{colors.undercut-wash}"
    textColor: "{colors.undercut}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  pill-ahead:
    backgroundColor: "{colors.ahead-wash}"
    textColor: "{colors.ahead}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  pill-flat:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.mute}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  note-undercut:
    backgroundColor: "{colors.undercut-wash}"
    textColor: "{colors.undercut-ink}"
    rounded: "{rounded.control}"
    padding: "7px 10px"
  note-ahead:
    backgroundColor: "{colors.ahead-wash}"
    textColor: "{colors.ahead-ink}"
    rounded: "{rounded.control}"
    padding: "7px 10px"
  note-flat:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.mute}"
    rounded: "{rounded.control}"
    padding: "7px 10px"
  note-failed:
    backgroundColor: "{colors.warning-wash}"
    textColor: "{colors.warning}"
    rounded: "{rounded.control}"
    padding: "7px 10px"
  link:
    backgroundColor: "{colors.card}"
    textColor: "{colors.accent}"
    rounded: "{rounded.link}"
    padding: "5px 10px"
  link-shop:
    backgroundColor: "{colors.accent-wash}"
    textColor: "{colors.accent}"
    rounded: "{rounded.link}"
    padding: "5px 10px"
  badge-undercut:
    backgroundColor: "{colors.undercut-wash}"
    textColor: "{colors.undercut}"
    rounded: "{rounded.badge}"
    padding: "3px 8px"
  badge-ahead:
    backgroundColor: "{colors.ahead-wash}"
    textColor: "{colors.ahead}"
    rounded: "{rounded.badge}"
    padding: "3px 8px"
  badge-flat:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.mute}"
    rounded: "{rounded.badge}"
    padding: "3px 8px"
  badge-failed:
    backgroundColor: "{colors.warning-wash}"
    textColor: "{colors.warning}"
    rounded: "{rounded.badge}"
    padding: "3px 8px"
---

# Design System: Price Radar

## Overview

**Creative North Star: "The Shop Bench"**

Price Radar is a light operate dashboard. The own shop price is the bench on every product card: a violet wash holds that price beside a small sparkline, marketplace rows sit under it as gaps, and a tinted sentence names the undercut. The ground is a cool grey, cards are white with a hairline and one soft shadow, and the loud color is the gap itself. Red means a marketplace is cheaper. Green means the shop is. Marketplace hues stay on the series dot and the chart stroke.

The page is a scan, dense and quiet. One sans, Inter, with the system stack behind it when Inter is not installed. Figures are tabular, in German formats. `color-scheme` is light. There is no dark theme.

The card does the job without a chart. The history chart opens in a side panel. The product photo sits in a rounded frame with the name beside it, and it carries no caption.

**Key Characteristics:**

- Cool grey ground, white cards, one shared soft shadow
- Violet marks the shop; red and green mark the gap
- Marketplace hues stay on the series, each with its own dash
- Inter at 14px, tabular prices and percents, German formats
- Shop block, marketplace rows, and the undercut sentence are the card

## Colors

The palette is a neutral tool surface, one violet for the shop, a red/green pair for the gap, and a fixed hue per marketplace.

### Primary

- **Signal Violet** (`#5b5bf6`): the shop. It colors the reference name, text links, the chart's shop stroke, focus rings, and the selection wash's pair. It is not a status color.
- **Violet Wash** (`#ececfe`): the shop block, the panel's shop comparison cell, the shop link at rest, link hover, and text selection.
- **Lifted Violet** (`#7c5cff`): only the far stop of the radar mark's 135° gradient, from Signal Violet to this.

### Secondary

- **Undercut Red** (`#e5484d`): a marketplace price below the shop, past −0.05%. Pill text, sparkline stroke, and KPI figures that are an undercut.
- **Undercut Wash** (`#fdecec`): the undercut pill, the undercut note, and the undercut badge.
- **Undercut Ink** (`#9f1239`): the undercut sentence. The pill uses Undercut Red; the sentence uses this darker ink.
- **Shop Green** (`#1f7a45`): a marketplace price above the shop, past +0.05%. Also the freshness dot beside the timestamp.
- **Green Wash** (`#e6f6ec`): the ahead pill, the ahead note, the ahead badge, and the 3px ring around the freshness dot.
- **Green Ink** (`#166534`): the ahead sentence ("Dein Shop ist am günstigsten").
- **Fetch Amber** (`#8a5a08`): a failed fetch, when there is no price to compare. Not Amazon's series color.
- **Amber Wash** (`#fdf3e1`): the failed-fetch note and badge.

### Tertiary

Series colors are fixed per marketplace in the generator's map, and they paint the row dot, the chart stroke, and that series' dash. They do not paint chrome.

- **Zalando Orange** (`#ff6900`), solid stroke.
- **Otto Red** (`#d4002a`), dash `6 4`.
- **Galeria Blue** (`#2a6ad8`), dash `2 3`.
- **Amazon Amber** (`#e07a00`), dash `8 3`. Distinct from Fetch Amber.
- **eBay Blue** (`#0064d2`), dash `2 2`.
- **About You Black** (`#111111`), dash `10 4 2 4`.
- **Kaufland Red** (`#e10915`), dash `4 3`.
- **Unassigned Slate** (`#5c6570`): any marketplace not in the map, dash `3 3`.

### Neutral

- **Cool Ground** (`#f7f7f8`): the page, and the side panel. Print sets the page to Card White.
- **Card White** (`#ffffff`): cards, KPIs, buttons, selects, menus, tooltips, panel boxes, and the photo frame.
- **Ink** (`#0b0b0f`): primary text and prices.
- **Mute Slate** (`#5c6370`): secondary text, flat pills, dates on a row, the sparkline's shop line, and the empty state.
- **Hairline** (`#e7e7eb`): the 1px border on cards, buttons, photos, menus, and chart gridlines.
- **Soft Fill** (`#f1f1f4`): segment tracks, button hover, flat notes, comparison cells that are not the shop, and menu hover.
- **Panel Scrim** (`rgba(8,8,14,.45)`): the overlay behind the side panel.

### Named Rules

**The Shop Bench Rule.** Violet is the own shop: the block, the chart series, the reference cell, and text links. Marketplace hues never color it, and violet never means "cheaper" or "failed."

**The Gap Rule.** A gap under −0.05% is Undercut Red. A gap over +0.05% is Shop Green. Inside that band the pill is Mute Slate on Soft Fill. A missing or failed price is a dash, never a guessed number. The sentence uses Undercut Ink or Green Ink, not the pill color.

**The Series Rule.** A marketplace keeps one hue and one dash on every card and on the chart. Amazon Amber and Fetch Amber stay different colors.

## Typography

**Display Font:** Inter (with ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif)
**Body Font:** Inter (same stack)
**Label/Mono Font:** ui-monospace, Menlo, monospace, for shop URLs only

**Character:** One sans for the whole tool. Inter is the face the mockup names; the system stack is the fallback, and the page does not load a font file. The CSS sets variable-face weights (550, 620, 650, 680) and Inter features `cv11` and `ss01`. Prices, percents, SKUs, and dates use tabular numerals.

### Hierarchy

- **Display** (650, 26px, line-height 1.45, −0.02em): KPI figures. Below 600px the same figure is 22px.
- **Headline** (680, 22px, −0.02em): the shop price inside the violet block. Panel comparison prices are 18px at weight 650.
- **Title** (620, 13.5px, line-height 1.3): the product name, clamped to two lines. The page name is 17px / 650 / −0.01em. The panel title is 19px / 650 / −0.01em.
- **Body** (400, 14px, line-height 1.45): the page default. Buttons and selects are 13px at weight 550. Notes are 12px at weight 550. The footer legend is 12px, line-height 1.5.
- **Label** (550, 12.5px): segment buttons, KPI labels, and marketplace rows. The shop reference name is 11.5px at weight 650 in Signal Violet. URLs are 10.5px monospace in Mute Slate, single line, ellipsis.

### Named Rules

**The One Face Rule.** Inter is the face. The system stack is only the fallback. Monospace is for the shop URL, because it is an identifier, and for nothing else.

**The Tabular Rule.** Prices, percents, SKUs, and dates set tabular numerals. Money uses a German format with two fraction digits and a trailing €. Percents use one fraction digit, a leading + when the marketplace is dearer, a true minus (−) when it is cheaper, and ± inside the flat band.

## Layout

The page is one centered column, max width 1360px, with 28px of horizontal padding. The header is a single row: radar mark, name and subtitle, a flexible spacer, the timestamp, and Exportieren. Four KPI cards follow, in a four-column grid with a 14px gap. A sticky filter bar holds marketplace segments, status segments, a sort select, a range segment, and a grid/list toggle. The product grid is `auto-fill` with a 300px minimum and a 14px gap. List view is one column. A 12px legend sits under the grid.

The rhythm inside a card is 14px of padding and 10px between photo, shop block, rows, and note. Rows stack 4px apart. The filter bar gaps controls by 10px.

At 900px the KPI grid becomes two columns. At 600px the column padding drops to 14px, the header wraps, the timestamp takes a full row, the KPI figure is 22px with 12px 14px of padding, the product grid is one column, the filter bar scrolls horizontally without wrapping (pulled to the screen edges), the panel padding is 18px, and the comparison grid is two columns. Print hides the filter bar, the export menu, the overlay, and the footer, drops card shadows, and lays the grid in two columns on a white page.

### Named Rules

**The Scan Grid Rule.** Product cards flow at a 300px minimum, 14px apart, inside the 1360px column. Below 600px they stack, and the filter bar scrolls sideways instead of wrapping.

## Elevation & Depth

Depth is a hairline plus one soft shadow on resting surfaces. Cards, KPIs, and panel boxes share that shadow. The filter bar does not float on a shadow; it blurs the ground behind it. Overlays (menu, tooltip, panel) use a deeper shadow. The scrim is a flat dark veil. Print removes shadows.

### Shadow Vocabulary

- **Resting** (`box-shadow: 0 1px 2px rgba(16,16,24,.04), 0 8px 24px rgba(16,16,24,.06)`): cards, KPI tiles, and panel boxes.
- **Segment selected** (`box-shadow: 0 1px 2px rgba(16,16,24,.08)`): the white pill inside a segment track.
- **Tooltip** (`box-shadow: 0 8px 24px rgba(16,16,24,.12)`): the chart tooltip.
- **Menu** (`box-shadow: 0 12px 32px rgba(16,16,24,.12)`): the export menu.
- **Panel** (`box-shadow: -20px 0 60px rgba(0,0,0,.18)`): the side panel, cast to the left.
- **Freshness ring** (`box-shadow: 0 0 0 3px #e6f6ec`): the 7px green dot beside the timestamp. It is a status mark, not a surface shadow.

### Named Rules

**The Resting Shadow Rule.** Cards, KPIs, and panel boxes share the resting shadow. Menus, tooltips, and the panel use their own deeper shadow. Do not invent a second resting shadow.

**The Bar Blur Rule.** The only backdrop blur is the sticky filter bar: the ground at 88% over transparent, blurred 10px. Cards stay opaque.

## Shapes

Corners are soft and stepped by role. Cards, KPIs, and panel boxes are 16px. The shop block, the photo frame, comparison cells, and the export menu are 12px. Buttons, selects, notes, and segment tracks are 9px, with the selected segment button at 7px. Link chips are 8px, badges are 6px, the radar mark and the tooltip are 10px. Gap pills are fully round. Series dots are 7px circles; badge dots are 6px.

Borders are a 1px hairline. The photo uses `object-fit: contain` inside the frame. The card lifts 2px on hover and mixes the border toward violet (40% Signal Violet, 60% Hairline), only when the user has not asked for reduced motion. The motion is 180ms, `cubic-bezier(.2,.7,.2,1)` on the lift and the border.

### Named Rules

**The Soft Corner Rule.** 16px for the card, 12px for an inset block, 9px for a control, full round for a gap pill. Do not square the cards, and do not round the page itself.

## Components

### Buttons

- **Shape:** gently rounded controls (9px). Height 34px. Label at 13px, weight 550, with a 7px gap to a 14px stroke icon.
- **Primary:** there is no filled primary button. Exportieren is Card White, Ink text, a hairline border, padding 0 12px.
- **Hover / Focus:** hover fills Soft Fill. Focus is the page ring: 2px Signal Violet, 2px offset.
- **Icon:** the square control is 34px by 34px, padding 0, used for close and for the grid/list icons inside a segment.

### Chips

- **Style:** gap pills are fully round, 12px, weight 650, padding 2px 8px. Undercut is Undercut Red on Undercut Wash. Ahead is Shop Green on Green Wash. Flat or missing is Mute Slate on Soft Fill, and the missing value is an en dash.
- **State:** status badges in the panel are the same three washes plus Fetch Amber, at 11.5px, weight 650, padding 3px 8px, radius 6px, with a 6px dot in the current text color.

### Cards / Containers

- **Corner Style:** 16px.
- **Background:** Card White on Cool Ground.
- **Shadow Strategy:** the resting shadow. Hover lifts the card 2px; it does not add a new shadow.
- **Border:** 1px Hairline. Hover mixes in 40% Signal Violet.
- **Internal Padding:** 14px, with 10px between the photo row, the shop block, the marketplace rows, and the note.
- **Photo:** 76px square (96px in the panel), 12px radius, hairline, contain. No caption. A missing image reads "kein Bild" at 11px in Mute Slate.
- **Rows:** name, price, and a 78px pill. The name carries a 7px series dot. A stale date sits in Mute Slate after the price.

### Inputs / Fields

- **Style:** the sort control is a native select, 34px tall, hairline, Card White, 9px radius, 13px type, padding 0 10px.
- **Focus:** the same 2px violet outline.
- **Error / Disabled:** a failed fetch is not a field error. It is the amber note and a dash in the pill.

### Navigation

The header is the only chrome. The radar mark is 34px, radius 10px, white stroke icon on a gradient from Signal Violet to Lifted Violet. The page name is 17px / 650 / −0.01em. The subtitle under it is 13px Mute Slate. The timestamp is 12.5px Mute Slate with the freshness dot. Exportieren opens a menu (radius 12px, padding 6px, min width 250px); items are 13px, radius 8px, padding 8px 10px, and hover fills Soft Fill. Item captions are 11.5px Mute Slate.

The filter bar sticks to the top of the column, z-index 5, and blurs the ground (see The Bar Blur Rule). Segments are a Soft Fill track with a hairline, radius 9px, padding 2px. The selected button is Card White, Ink, radius 7px, with the segment shadow. Unselected buttons are Mute Slate.

The side panel is a dialog on the scrim, up to 880px wide, Cool Ground, hairline on the left, padding 24px 28px. Link chips are 12.5px Signal Violet, hairline, Card White, radius 8px, padding 5px 10px; the shop link and every link hover use Violet Wash.

### Shop block

The signature. Violet Wash, radius 12px, padding 10px 12px. The reference name is Signal Violet at 11.5px / 650. The price is the headline figure, tabular. The sparkline takes about 46% of the row, at least 120px wide. It plots the cheapest marketplace in the selected range: stroke 1.6px, Undercut Red, Shop Green, or Mute Slate by The Gap Rule. The shop price on that spark is a muted dashed line (`3 3`), not the violet chart stroke. With fewer than two points the spark reads "noch kein Verlauf."

### Undercut note

The sentence under the rows. Radius 9px, padding 7px 10px, 12px at weight 550, with a 12px stroke icon. Undercut uses Undercut Wash and Undercut Ink and names the cheapest marketplace, the German percent, and how many others sit below. Ahead uses Green Wash and Green Ink. No price yet uses Soft Fill and Mute Slate. A failed fetch with no stored price uses Amber Wash and Fetch Amber.

### KPI tile

Four tiles. Mute label at 12.5px, the display figure, then a 12px mute hint. An undercut figure is Undercut Red. A negative average gap is Undercut Red; a positive one is Shop Green.

### Chart

Lives in the panel, not on the card. Marketplace strokes are 2px in the series hue and dash. The shop history is a 2.4px Signal Violet stroke. Gridlines are Hairline; axis labels are 11px Mute Slate. The tooltip is Card White, hairline, radius 10px, 12px type, the tooltip shadow. A single shop price with no history is a violet rule with a small violet label.

### Named Rules

**The Sparkline Rule.** On the card, the sparkline is the cheapest marketplace, colored by the gap, and the dashed mute line is the shop price. On the panel chart, the shop series is the violet stroke and each marketplace keeps its own hue and dash.

## Do's and Don'ts

### Do:

- **Do** keep the ground cool grey and the cards white, with the shared resting shadow.
- **Do** measure every marketplace price against the shop price, and show the gap as red, green, or mute.
- **Do** keep each marketplace on its fixed hue and dash, on the row dot and on the chart.
- **Do** show a missing or failed price as missing: a dash in the pill, and a mute or amber note. Never a filled-in number.
- **Do** draw icons as stroke SVGs in `currentColor`, at stroke 2 or 2.2.
- **Do** use the violet focus ring (2px outline, 2px offset) and the violet selection wash.

### Don't:

- **Don't** add a dark theme. The page sets light `color-scheme` only.
- **Don't** color buttons, notes, KPI chrome, or the page ground with a marketplace hue.
- **Don't** replace the shop block, the rows, and the undercut sentence with a chart on the card. The history chart belongs in the panel.
- **Don't** introduce a second display face. Inter is first; the system stack is the fallback.
- **Don't** caption the product photo. The name sits beside the frame.
- **Don't** use emoji or a unicode bullet as an icon. Icons are stroke SVGs.
