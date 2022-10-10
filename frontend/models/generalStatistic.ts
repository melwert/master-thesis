export interface GeneralStatistic {
    id: string,
    commitCount: number,
    fileCount: number,
    developerCount: number,
    repositoryLink: string,
    bitbucketCommentCount: number,
    bitbucketPrCount: number,
    branchCount: number,
    jiraIssueCount: number,
    fileEndings: string[],
    lastScanDate: Date,
}