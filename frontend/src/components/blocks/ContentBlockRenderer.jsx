import TextBlock from './TextBlock'
import DocumentBlock from './DocumentBlock'
import YoutubeBlock from './YoutubeBlock'

export default function ContentBlockRenderer({ block }) {
  switch (block.type) {
    case 'text':     return <TextBlock block={block} />
    case 'document': return <DocumentBlock block={block} />
    case 'youtube':  return <YoutubeBlock block={block} />
    default:         return null
  }
}
