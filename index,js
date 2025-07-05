// index.js
require('dotenv').config();
const { Client, GatewayIntentBits, ChannelType } = require('discord.js');
const Parser = require('rss-parser');
const parser = new Parser();

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages]
});

const FEEDS = {
  'Beyond-All-Reason': 'https://www.beyondallreason.info/rss',
  'Crossout': 'https://crossout.net/en/rss/',
  'Destiny 2': 'https://www.bungie.net/en/Rss/News.aspx',
  'Fall Guys': 'https://fallguys.com/en/news/rss',
  'Lethal Company': 'https://store.steampowered.com/feeds/news/app/1966720/',
  'Once Human': 'https://oncehuman.game/rss',
  'The Planet Crafter': 'https://store.steampowered.com/feeds/news/app/1284190/',
  'Risk of Rain 2': 'https://store.steampowered.com/feeds/news/app/632360/',
  'Smite 2': 'https://www.smitegame.com/news/feed',
  'Warframe': 'https://www.warframe.com/news?format=rss'
};

const postedItems = new Set();

client.once('ready', async () => {
  console.log(`Logged in as ${client.user.tag}`);

  const guild = client.guilds.cache.first();

  for (const [game, feedUrl] of Object.entries(FEEDS)) {
    const categoryName = `${game}`;
    let category = guild.channels.cache.find(c => c.name === categoryName.toLowerCase() && c.type === ChannelType.GuildCategory);

    if (!category) {
      category = await guild.channels.create({
        name: categoryName,
        type: ChannelType.GuildCategory
      });
    }

    let newsChannel = guild.channels.cache.find(c => c.name === `${game.toLowerCase().replace(/ /g, '-')}-news`);

    if (!newsChannel) {
      newsChannel = await guild.channels.create({
        name: `${game.toLowerCase().replace(/ /g, '-')}-news`,
        type: ChannelType.GuildText,
        parent: category.id,
        permissionOverwrites: []
      });
    }
  }

  setInterval(checkFeeds, 5 * 60 * 1000); // every 5 minutes
});

async function checkFeeds() {
  for (const [game, feedUrl] of Object.entries(FEEDS)) {
    try {
      const feed = await parser.parseURL(feedUrl);
      const guild = client.guilds.cache.first();
      const newsChannel = guild.channels.cache.find(c => c.name === `${game.toLowerCase().replace(/ /g, '-')}-news`);

      if (!feed || !feed.items || !newsChannel) continue;

      for (const item of feed.items.slice(0, 3)) {
        const uniqueId = `${game}-${item.link}`;
        if (postedItems.has(uniqueId)) continue;
        postedItems.add(uniqueId);

        await newsChannel.send(`📰 **${game} Update:** [${item.title}](${item.link})`);
      }
    } catch (err) {
      console.error(`Failed to fetch feed for ${game}:`, err.message);
    }
  }
}

client.login(process.env.DISCORD_TOKEN);
