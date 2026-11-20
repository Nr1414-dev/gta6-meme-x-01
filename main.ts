// Entry for the make.fun bounty "Post a GTA 6 meme on X" (gta6-meme-x-01).
// Reads POST.json and writes a copy to output/POST.json.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const post = JSON.parse(readFileSync(new URL("./POST.json", import.meta.url), "utf-8"));
mkdirSync("output", { recursive: true });
writeFileSync("output/POST.json", JSON.stringify(post, null, 2));
console.log(post.url);
