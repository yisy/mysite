<template>
  <b-col cols="8">
    <b-card :header="article.title">
      <p class="card-text"><vue-markdown class="markdown-body">{{article.markdown_content}}</vue-markdown></p>
      <p class="card-text text-muted">
        <timeago :datetime="article.created_time" locale="zh-CN" class="text-muted"></timeago>
        <span class="text-muted pull-right">
          <i class="fa fa-eye"> {{article.view}}</i>
          <i class="fa fa-comments"> {{comments_count}}</i>
        </span>
      </p>
    </b-card>
    <br>
    <comment :comments="article.comments" :article_id='article.id' ref="comment"></comment>
  </b-col>
</template>

<script>
import comment from '@/components/section/comment'
import { getarticle } from '@/api/api'
import VueMarkdown from 'vue-markdown'

export default {
  data () {
    return {
      article: [],
      article_id: this.$route.params.id,
      comments_count: 0
    }
  },
  created () {
    this.get_article()
  },
  components: {
    'comment': comment,
    VueMarkdown
  },
  methods: {
    get_article () {
      getarticle(this.article_id)
        .then(response => {
          this.article = response.data
          this.comments_count = this.article.comments.length
          document.title = response.data.title + ' - 何人也的博客'
        })
        .catch(error => {
          console.log(error.response.status)
          this.$router.push({ name: '404' })
        })
    }
  }
}
</script>
